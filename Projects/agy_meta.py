#!/usr/bin/env python3
import os
import json
import sys
from glob import glob
from urllib.parse import unquote

def list_valid_projects():
    projects_dir = os.path.expanduser("~/.gemini/config/projects")
    gemini_projects_root = os.path.expanduser("~/.gemini/Projects")
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
    projects_dir = os.path.expanduser("~/.gemini/config/projects")
    gemini_projects_root = os.path.expanduser("~/.gemini/Projects")
    
    name_mappings = {}
    path_mappings = {}
    id_mappings = {}

    for json_file in glob(os.path.join(projects_dir, "*.json")):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                pid = data.get("id")
                raw_name = data.get("name", "")
                if not raw_name or not pid:
                    continue
                safe_name = os.path.basename(raw_name.rstrip('/'))
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

    q = os.path.expandvars(str(query).strip())
    target_pid = None
    target_name = None

    # 1. Match by project ID
    if q in id_mappings:
        target_pid, target_name = id_mappings[q]
    # 2. Match by exact or case-insensitive project name
    elif q.lower() in name_mappings:
        target_pid, target_name = name_mappings[q.lower()]
    # 3. Match by directory path if path-like
    elif q.startswith(("/", "~", "./", "../")) or os.path.isabs(q) or os.path.exists(q):
        curr = os.path.abspath(os.path.expanduser(q))
        while curr != "/":
            if curr in path_mappings:
                target_pid, target_name = path_mappings[curr]
                break
            curr = os.path.dirname(curr)

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
        fallback = os.path.expanduser(f"~/.gemini/Projects/{os.path.basename(os.path.abspath(query))}")
        print(fallback)
        sys.exit(0)
