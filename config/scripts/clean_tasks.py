# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
import os
import glob
import re
import yaml

PROJECTS_ROOT = os.path.expanduser("~/.gemini/Projects")

STATUS_MAP = {
    "todo": "backlog",
    "pending": "backlog",
    "open": "backlog",
    "in_progress": "active",
    "review": "in_review",
    "ready_for_review": "in_review",
    "done": "completed",
    "closed": "completed",
    "resolved": "completed"
}

def parse_frontmatter(content: str):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1)), match.group(2)
    return {}, content

def format_frontmatter(metadata: dict, body: str) -> str:
    fm = yaml.dump(metadata, sort_keys=False, allow_unicode=True)
    return f"---\n{fm}---\n{body}"

def clean_tasks():
    cleaned_count = 0
    for project in os.listdir(PROJECTS_ROOT):
        tasks_dir = os.path.join(PROJECTS_ROOT, project, "tasks")
        if not os.path.isdir(tasks_dir):
            continue
            
        for file_path in glob.glob(os.path.join(tasks_dir, "*.md")):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            meta, body = parse_frontmatter(content)
            if not meta or "status" not in meta:
                continue
                
            old_status = str(meta["status"]).strip("'\"").lower()
            new_status = STATUS_MAP.get(old_status, old_status)
            
            if old_status != new_status or meta["status"] != new_status:
                meta["status"] = new_status
                new_content = format_frontmatter(meta, body)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                cleaned_count += 1
                print(f"Cleaned [{project}] {os.path.basename(file_path)}: {old_status} -> {new_status}")
                
    print(f"Cleanup complete. Total {cleaned_count} files normalized.")

if __name__ == "__main__":
    clean_tasks()
