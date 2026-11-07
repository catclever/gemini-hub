#!/usr/bin/env python3
import os
import json
import sys
from glob import glob
from urllib.parse import unquote


def _resolve_gemini_roots() -> tuple[str, str]:
    """
    Resolves (gemini_projects_root, projects_dir) across Mac, PVE Linux,
    and Google Cloud Remote Agent sandboxes (/workspace/gemini-hub).
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.environ.get("PROJECTS_ROOT"),
        script_dir,
        "/workspace/gemini-hub/Projects",
        os.path.expanduser("~/.gemini/Projects"),
    ]

    gemini_projects_root = None
    for cand in candidates:
        if cand and os.path.isdir(cand):
            gemini_projects_root = os.path.abspath(cand)
            break

    if not gemini_projects_root:
        gemini_projects_root = os.path.expanduser("~/.gemini/Projects")

    hub_root = os.path.dirname(gemini_projects_root)
    candidate_projects_cfg = os.path.join(hub_root, "config", "projects")
    if os.path.isdir(candidate_projects_cfg):
        projects_dir = candidate_projects_cfg
    else:
        projects_dir = os.path.expanduser("~/.gemini/config/projects")

    return gemini_projects_root, projects_dir


def list_valid_projects():
    gemini_projects_root, projects_dir = _resolve_gemini_roots()
    valid = set()
    for json_file in glob(os.path.join(projects_dir, "*.json")):
        try:
            with open(json_file, "r") as f:
                data = json.load(f)
                name = data.get("name")
                if name and name != "Outside of Project":
                    valid.add(os.path.basename(name.rstrip("/")))
        except Exception:
            pass
    if os.path.exists(gemini_projects_root):
        for item in os.listdir(gemini_projects_root):
            item_path = os.path.join(gemini_projects_root, item)
            if os.path.isdir(item_path) and not item.startswith((".", "_")):
                valid.add(item)
    return sorted(list(valid))


def get_meta_dir(query):
    gemini_projects_root, projects_dir = _resolve_gemini_roots()

    name_mappings = {}
    path_mappings = {}
    id_mappings = {}

    for json_file in glob(os.path.join(projects_dir, "*.json")):
        try:
            with open(json_file, "r") as f:
                data = json.load(f)
                pid = data.get("id")
                raw_name = data.get("name", "")
                if not raw_name or not pid:
                    continue
                safe_name = os.path.basename(raw_name.rstrip("/"))
                name_mappings[safe_name.lower()] = (pid, safe_name)
                id_mappings[pid] = (pid, safe_name)

                resources = data.get("projectResources", {}).get("resources", [])
                for res in resources:
                    uri = res.get("gitFolder", {}).get("folderUri", "") or res.get("folderUri", "")
                    if uri.startswith("file://"):
                        path = unquote(uri[7:])
                        path_mappings[os.path.abspath(path)] = (pid, safe_name)
        except Exception:
            continue

    if os.path.exists(gemini_projects_root):
        for item in os.listdir(gemini_projects_root):
            item_path = os.path.join(gemini_projects_root, item)
            if os.path.isdir(item_path) and not item.startswith((".", "_")):
                if item.lower() not in name_mappings:
                    pid = None
                    id_file = os.path.join(item_path, ".project_id")
                    if os.path.exists(id_file):
                        try:
                            with open(id_file, "r") as f:
                                pid = f.read().strip()
                        except Exception:
                            pass
                    name_mappings[item.lower()] = (pid or item, item)

    # Known repository alias: catclever/gemini-hub -> gemini
    if "gemini" in name_mappings and "gemini-hub" not in name_mappings:
        name_mappings["gemini-hub"] = name_mappings["gemini"]

    q = os.path.expandvars(str(query).strip())
    target_pid = None
    target_name = None

    # 1. Match by project ID
    if q in id_mappings:
        target_pid, target_name = id_mappings[q]
    # 2. Match by exact or case-insensitive project name
    elif q.lower() in name_mappings:
        target_pid, target_name = name_mappings[q.lower()]
    # 3. Match by GitHub owner/repo slug (e.g., "catclever/Finnegan")
    elif (
        "/" in q
        and not q.startswith(("/", "~", "./", "../"))
        and len(q.strip("/").split("/")) == 2
    ):
        repo_slug = q.strip("/").split("/")[-1].lower()
        if repo_slug.endswith(".git"):
            repo_slug = repo_slug[:-4]
        if repo_slug in name_mappings:
            target_pid, target_name = name_mappings[repo_slug]
    # 4. Match by directory path if path-like (Mac, PVE /root/Projects, Cloud /workspace)
    elif q.startswith(("/", "~", "./", "../")) or os.path.isabs(q) or os.path.exists(q):
        curr = os.path.abspath(os.path.expanduser(q))
        while curr != "/":
            if curr in path_mappings:
                target_pid, target_name = path_mappings[curr]
                break
            curr = os.path.dirname(curr)

        # Cloud Remote Agent (/workspace/<project>) or PVE (/root/Projects/<project>) fallback
        if not target_name:
            norm_path = os.path.abspath(os.path.expanduser(q))
            for prefix in ("/workspace/", "/root/Projects/"):
                if norm_path.startswith(prefix):
                    rel = norm_path[len(prefix):].strip("/")
                    if rel:
                        first_seg = rel.split("/")[0].lower()
                        if first_seg in name_mappings:
                            target_pid, target_name = name_mappings[first_seg]
                            break

    if not target_name:
        return ""

    target_dir = os.path.join(gemini_projects_root, target_name)

    if not os.path.exists(gemini_projects_root):
        os.makedirs(gemini_projects_root)

    # Auto-healing: Look for an existing folder with the same project ID
    if target_pid:
        for folder in os.listdir(gemini_projects_root):
            folder_path = os.path.join(gemini_projects_root, folder)
            if not os.path.isdir(folder_path):
                continue

            id_file = os.path.join(folder_path, ".project_id")
            if os.path.exists(id_file):
                with open(id_file, "r") as f:
                    saved_id = f.read().strip()
                # If ID matches but name doesn't, we caught a rename event!
                if saved_id == target_pid and folder != target_name:
                    if not os.path.exists(target_dir):
                        os.rename(folder_path, target_dir)
                    break

    # Ensure target dir exists and seed the ID for future tracking
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    if target_pid:
        id_file = os.path.join(target_dir, ".project_id")
        if not os.path.exists(id_file):
            with open(id_file, "w") as f:
                f.write(target_pid)

    return target_dir


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    result = get_meta_dir(query)
    if result:
        print(result)
        sys.exit(0)
    else:
        # Fallback to the basename of the current directory if no mapping found
        gemini_projects_root, _ = _resolve_gemini_roots()
        fallback = os.path.join(gemini_projects_root, os.path.basename(os.path.abspath(query)))
        print(fallback)
        sys.exit(0)
