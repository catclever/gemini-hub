# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "mcp",
#     "pyyaml"
# ]
# ///

import os
import sys
import glob
import re
import yaml
from mcp.server.mcpserver import MCPServer
from typing import Literal

# Ensure agy_meta can be imported across Mac, PVE Linux, and Cloud containers
for _candidate_path in (
    os.environ.get("PROJECTS_ROOT"),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Projects")),
    "/workspace/gemini-hub/Projects",
    os.path.expanduser("~/.gemini/Projects"),
):
    if _candidate_path and _candidate_path not in sys.path:
        sys.path.append(_candidate_path)

import agy_meta

# Enforced strict schemas
StatusEnum = Literal['backlog', 'active', 'in_review', 'completed']
PriorityEnum = Literal['low', 'medium', 'high']

VALID_STATUSES = {'backlog', 'active', 'in_review', 'completed'}

STATUS_MAPPING = {
    # Backlog synonyms
    "todo": "backlog", "to-do": "backlog", "to_do": "backlog", "pending": "backlog",
    "open": "backlog", "planned": "backlog", "draft": "backlog", "queued": "backlog",
    "new": "backlog", "blocked": "backlog",

    # Active synonyms
    "in_progress": "active", "in-progress": "active", "in progress": "active",
    "progress": "active", "doing": "active", "running": "active", "wip": "active",
    "started": "active", "ongoing": "active",

    # In Review synonyms
    "review": "in_review", "reviewing": "in_review", "in-review": "in_review",
    "in review": "in_review", "testing": "in_review", "qa": "in_review",
    "verify": "in_review", "verifying": "in_review",

    # Completed synonyms
    "done": "completed", "finished": "completed", "complete": "completed",
    "closed": "completed", "resolved": "completed", "merged": "completed",
    "success": "completed", "passed": "completed"
}

def normalize_status_value(raw: any) -> str:
    if raw is None:
        return "backlog"
    norm = str(raw).strip().lower().replace(" ", "_").replace("-", "_")
    if norm in VALID_STATUSES:
        return norm
    if norm in STATUS_MAPPING:
        return STATUS_MAPPING[norm]
    return "backlog"

mcp = MCPServer("KanbanTaskManager")

def resolve_project_tasks_dir(project: str) -> tuple[str, str]:
    if not project or not str(project).strip():
        raise ValueError("Project identifier or workspace path cannot be empty.")
    
    meta_dir = agy_meta.get_meta_dir(project)
    if not meta_dir or not os.path.exists(meta_dir):
        valid_projects = agy_meta.list_valid_projects()
        sample = ", ".join(valid_projects[:10]) + ("..." if len(valid_projects) > 10 else "")
        raise ValueError(
            f"Invalid project or workspace path '{project}'. "
            f"Could not resolve canonical metadata directory via agy_meta.py. "
            f"Available valid projects: [{sample}]"
        )
    
    canonical_name = os.path.basename(meta_dir)
    tasks_dir = os.path.join(meta_dir, "tasks")
    os.makedirs(tasks_dir, exist_ok=True)
    return canonical_name, tasks_dir

def parse_frontmatter(content: str):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1)), match.group(2)
    return {}, content

def format_frontmatter(metadata: dict, body: str) -> str:
    fm = yaml.dump(metadata, sort_keys=False, allow_unicode=True)
    body_str = body.strip()
    if body_str:
        return f"---\n{fm}---\n\n{body_str}\n"
    return f"---\n{fm}---\n"

def generate_default_task_body(title: str, status: str, description: str = "") -> str:
    """Generates standard Markdown body for a task card."""
    t = title.strip() or "Untitled Task"
    desc = description.strip() if description else ""
    
    if desc:
        if desc.startswith("#"):
            return f"{desc}\n"
        if status == "completed":
            return (
                f"# {t}\n\n"
                f"## 变更概述\n"
                f"{desc}\n\n"
                f"## 验证结论\n"
                f"- [x] 核心逻辑已实现并通过验证\n"
            )
        else:
            return (
                f"# {t}\n\n"
                f"## 任务目标与背景\n"
                f"{desc}\n\n"
                f"## 实施要点\n"
                f"<!-- 涉及的核心模块、关键逻辑或接口定义 -->\n\n"
                f"## 交付验收清单\n"
                f"- [ ] 核心实现步骤 1\n"
            )
    else:
        if status == "completed":
            return (
                f"# {t}\n\n"
                f"## 变更概述\n"
                f"完成核心功能改造与验证。\n\n"
                f"## 验证结论\n"
                f"- [x] 核心逻辑已实现并通过验证\n"
            )
        else:
            return (
                f"# {t}\n\n"
                f"## 任务目标与背景\n"
                f"待补充具体需求背景。\n\n"
                f"## 实施要点\n"
                f"<!-- 涉及的核心模块、关键逻辑或接口定义 -->\n\n"
                f"## 交付验收清单\n"
                f"- [ ] 核心实现步骤 1\n"
            )

@mcp.tool()
def list_tasks(project: str) -> str:
    """List all tasks and their exact statuses for a specific project or workspace path."""
    try:
        canonical_name, tasks_dir = resolve_project_tasks_dir(project)
    except ValueError as e:
        return f"Error: {e}"
    
    results = []
    for file_path in sorted(glob.glob(os.path.join(tasks_dir, "*.md"))):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            meta, _ = parse_frontmatter(content)
            if meta:
                task_id = meta.get("id", os.path.basename(file_path).replace(".md", ""))
                status = meta.get("status", "unknown")
                title = meta.get("title", "Untitled")
                results.append(f"[{task_id}] {title} (Status: {status})")
    return "\n".join(results) if results else f"No tasks found for project '{canonical_name}'."

def clean_task_slug(task_id: str, title: str = "") -> str:
    """Strips manual task numbers, prefixes, suffixes, and normalizes into a clean snake_case slug."""
    if not task_id:
        slug = ""
    else:
        s = str(task_id).strip().lower()
        # Remove file extension if present
        s = re.sub(r"\.md$", "", s)
        # Remove prefix numbers like task_001_, task-001-, 001_, t-001_, etc.
        s = re.sub(r"^(?:task|t)?[-_]?\d+[-_]?", "", s)
        # Remove suffix numbers like _001, -001, _1, -1, _056, etc.
        s = re.sub(r"[-_](?:task|t)?\d+$", "", s)
        # Replace non-alphanumeric (except underscores and hyphens) with underscore
        s = re.sub(r"[^\w\-]+", "_", s)
        # Normalize multiple underscores/hyphens
        s = re.sub(r"[-_]+", "_", s).strip("_-")
        slug = s

    if not slug and title:
        # Fallback to slugifying title
        s = str(title).strip().lower()
        s = re.sub(r"[^\w\s\-]+", "", s)
        s = re.sub(r"[\s\-]+", "_", s).strip("_-")
        slug = s

    return slug or "task"

def get_next_task_number(tasks_dir: str) -> int:
    """Finds the highest sequence number in tasks_dir and returns next number (max + 1)."""
    max_num = 0
    if not os.path.exists(tasks_dir):
        return 1
    
    for f in os.listdir(tasks_dir):
        if not f.endswith(".md"):
            continue
        # Check suffix like _056.md or -056.md
        m = re.search(r"[-_](\d+)\.md$", f)
        if m:
            max_num = max(max_num, int(m.group(1)))
            continue
        # Check prefix like task_001_...md or 001_...md
        m = re.search(r"^(?:task[-_]?)?(\d+)[-_]", f)
        if m:
            max_num = max(max_num, int(m.group(1)))
            continue
            
    return max_num + 1

def find_task_file(tasks_dir: str, task_id: str) -> tuple[str, str]:
    """
    Locates task file in tasks_dir.
    Returns (actual_task_id, file_path) or (None, None).
    Supports:
    1. Exact match: task_id.md
    2. Number match: e.g. "057" or "57" -> *_057.md
    3. Slug match: e.g. "backend_temp_card_expiration" -> backend_temp_card_expiration_*.md
    """
    if not os.path.exists(tasks_dir):
        return None, None

    clean_id = str(task_id).strip()
    if clean_id.endswith(".md"):
        clean_id = clean_id[:-3]
        
    exact_path = os.path.join(tasks_dir, f"{clean_id}.md")
    if os.path.exists(exact_path):
        return clean_id, exact_path
        
    # Check if task_id is a number or "task_XX"
    num_match = re.match(r"^(?:task[-_]?)?(\d+)$", clean_id, re.IGNORECASE)
    if num_match:
        target_num = int(num_match.group(1))
        for f in os.listdir(tasks_dir):
            if not f.endswith(".md"):
                continue
            m = re.search(r"[-_](\d+)\.md$", f) or re.search(r"^(?:task[-_]?)?(\d+)[-_]", f)
            if m and int(m.group(1)) == target_num:
                found_id = f[:-3]
                return found_id, os.path.join(tasks_dir, f)
                
    # Check if task_id matches slug (without sequence number)
    slug = clean_task_slug(clean_id)
    matches = []
    for f in os.listdir(tasks_dir):
        if not f.endswith(".md"):
            continue
        stem = f[:-3]
        if clean_task_slug(stem) == slug:
            matches.append((stem, os.path.join(tasks_dir, f)))
            
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        # Return highest sequence number / most recent
        matches.sort(key=lambda x: x[0], reverse=True)
        return matches[0]

    return None, None

@mcp.tool()
def update_task_status(project: str, task_id: str, status: StatusEnum) -> str:
    """Update the status of a specific task with strict enumeration checking."""
    try:
        canonical_name, tasks_dir = resolve_project_tasks_dir(project)
    except ValueError as e:
        return f"Error: {e}"
    
    actual_task_id, file_path = find_task_file(tasks_dir, task_id)
    if not file_path or not os.path.exists(file_path):
        return f"Error: Task '{task_id}' not found in project '{canonical_name}' ({tasks_dir})."
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    meta, body = parse_frontmatter(content)
    meta["status"] = status
    
    new_content = format_frontmatter(meta, body)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    return f"Successfully updated [{canonical_name}] {actual_task_id} status to '{status}'."

@mcp.tool()
def create_task(
    project: str,
    task_id: str = "",
    title: str = "",
    status: StatusEnum = 'backlog',
    priority: PriorityEnum = 'medium',
    tags: list[str] = None,
    session: str = None,
    description: str = ""
) -> str:
    """Create a new task in the Kanban board with strictly enforced schema, automatic sequence numbering, and rich markdown scaffolding.
    NOTE: Do NOT manually write task sequence numbers (e.g. _001, _042) in task_id;
    the MCP server will automatically strip any manual numbers and assign the next sequential number."""
    try:
        canonical_name, tasks_dir = resolve_project_tasks_dir(project)
    except ValueError as e:
        return f"Error: {e}"
    
    clean_slug = clean_task_slug(task_id, title)
    next_num = get_next_task_number(tasks_dir)
    final_task_id = f"{clean_slug}_{next_num:03d}"
    
    # Avoid collision in rare edge cases
    while os.path.exists(os.path.join(tasks_dir, f"{final_task_id}.md")):
        next_num += 1
        final_task_id = f"{clean_slug}_{next_num:03d}"
    
    file_path = os.path.join(tasks_dir, f"{final_task_id}.md")
    final_title = title or clean_slug.replace("_", " ").title()
    
    meta = {
        "id": final_task_id,
        "title": final_title,
        "status": status,
        "priority": priority,
        "tags": tags or [],
        "session": session
    }
    
    body = generate_default_task_body(final_title, status, description)
    new_content = format_frontmatter(meta, body)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    return f"Successfully created task [{canonical_name}] {final_task_id} (assigned #{next_num:03d})."

@mcp.tool()
def update_task_content(
    project: str,
    task_id: str,
    content: str,
    mode: Literal['append', 'replace'] = 'append'
) -> str:
    """Update or append markdown content to an existing task card.
    
    Args:
        project: Project name or workspace path.
        task_id: Task ID, bare slug, or task sequence number.
        content: Markdown content to append or replace.
        mode: 'append' to add to existing content, 'replace' to overwrite the markdown body.
    """
    try:
        canonical_name, tasks_dir = resolve_project_tasks_dir(project)
    except ValueError as e:
        return f"Error: {e}"
        
    actual_task_id, file_path = find_task_file(tasks_dir, task_id)
    if not file_path or not os.path.exists(file_path):
        return f"Error: Task '{task_id}' not found in project '{canonical_name}' ({tasks_dir})."
        
    with open(file_path, "r", encoding="utf-8") as f:
        file_text = f.read()
        
    meta, body = parse_frontmatter(file_text)
    
    if mode == 'replace':
        new_body = content.strip() + "\n"
    else:
        existing = body.strip()
        addition = content.strip()
        if existing:
            new_body = f"{existing}\n\n{addition}\n"
        else:
            title = meta.get("title", actual_task_id)
            new_body = f"# {title}\n\n{addition}\n"
            
    new_content = format_frontmatter(meta, new_body)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    return f"Successfully updated content for [{canonical_name}] {actual_task_id} (mode: {mode})."

@mcp.tool()
def normalize_all_tasks() -> str:
    """Scan all project task markdown files across ~/.gemini/Projects and fix invalid status fields, missing frontmatters, and empty bodies."""
    if hasattr(agy_meta, "_resolve_gemini_roots"):
        projects_root, _ = agy_meta._resolve_gemini_roots()
    else:
        projects_root = os.path.expanduser("~/.gemini/Projects")
    pattern = os.path.join(projects_root, "*", "tasks", "*.md")
    files = glob.glob(pattern)
    
    fixed_count = 0
    total_count = len(files)
    details = []

    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            meta, body = parse_frontmatter(content)
            modified = False

            if not meta:
                task_id = os.path.basename(file_path).replace(".md", "")
                title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                title = title_match.group(1).strip() if title_match else task_id
                
                checked_boxes = content.count("- [x]")
                unchecked_boxes = content.count("- [ ]")
                status = "completed" if (checked_boxes > 0 and unchecked_boxes == 0) else "backlog"

                meta = {
                    "id": task_id,
                    "title": title,
                    "status": status,
                    "priority": "medium",
                    "tags": []
                }
                body = content.strip() if content.strip() else generate_default_task_body(title, status)
                modified = True
                details.append(f"Synthesized frontmatter for {os.path.relpath(file_path, projects_root)} (status: {status})")
            else:
                task_id = os.path.basename(file_path).replace(".md", "")
                if not meta.get("id"):
                    meta["id"] = task_id
                    modified = True
                    details.append(f"Injected missing id '{task_id}' into {os.path.relpath(file_path, projects_root)}")

                current_status = meta.get("status")
                normalized_status = normalize_status_value(current_status)

                raw_status_match = re.search(r"^status:\s*(.+)$", content, re.MULTILINE)
                raw_val = raw_status_match.group(1).strip() if raw_status_match else ""

                if current_status != normalized_status or raw_val != normalized_status:
                    meta["status"] = normalized_status
                    modified = True
                    details.append(f"Normalized {os.path.relpath(file_path, projects_root)}: '{raw_val or current_status}' -> '{normalized_status}'")

                # Auto-heal empty body
                if not body or not body.strip():
                    title = meta.get("title", task_id)
                    body = generate_default_task_body(title, normalized_status)
                    modified = True
                    details.append(f"Synthesized body scaffold for {os.path.relpath(file_path, projects_root)}")

            if modified:
                new_content = format_frontmatter(meta, body)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                fixed_count += 1
        except Exception as e:
            sys.stderr.write(f"[KanbanMCP] Error processing {file_path}: {e}\n")

    summary = f"Scanned {total_count} tasks across all projects; normalized {fixed_count} task(s)."
    if details:
        summary += "\n" + "\n".join(f" - {d}" for d in details)
    sys.stderr.write(f"[KanbanMCP Startup] {summary}\n")
    return summary

if __name__ == "__main__":
    normalize_all_tasks()
    mcp.run()
