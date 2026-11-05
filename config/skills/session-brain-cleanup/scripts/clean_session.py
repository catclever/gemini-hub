#!/usr/bin/env python3
import os
import sys
import shutil
import stat
import argparse

def remove_readonly(func, path, excinfo):
    """Error handler for shutil.rmtree to handle readonly files (common in gocache/git)."""
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        print(f"  [Warning] Could not force remove {path}: {e}")

def clean_directory_contents(target_dir, label):
    """Safely cleans all contents inside a directory, leaving the directory itself intact."""
    if not os.path.exists(target_dir):
        return 0
    cleaned = 0
    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path, onerror=remove_readonly)
            else:
                os.remove(item_path)
            cleaned += 1
        except Exception as e:
            print(f"  [Error] Failed to remove {item_path}: {e}")
    if cleaned > 0:
        print(f"✓ Cleaned {cleaned} item(s) from {label} ({target_dir})")
    return cleaned

def clean_brain(conversation_id, clean_artifacts=False):
    brain_dir = os.path.expanduser(f"~/.gemini/antigravity/brain/{conversation_id}")
    
    if not os.path.exists(brain_dir):
        print(f"[Error] Session brain directory not found: {brain_dir}")
        return False

    print(f"=== Session Brain Cleanup 2.0 ===")
    print(f"Target Session : {conversation_id}")
    print(f"Brain Path     : {brain_dir}")
    print(f"Mode           : {'Full Reset (--all: removing artifacts)' if clean_artifacts else 'Safe Standard Cleanup (preserving markdown artifacts)'}")
    print("-" * 50)

    # 1. Clean scratch/ directory
    scratch_dir = os.path.join(brain_dir, "scratch")
    clean_directory_contents(scratch_dir, "scratch directory")

    # 2. Clean .tempmediaStorage/ directory
    media_dir = os.path.join(brain_dir, ".tempmediaStorage")
    if os.path.exists(media_dir):
        try:
            shutil.rmtree(media_dir, onerror=remove_readonly)
            print(f"✓ Removed temporary media cache directory: {media_dir}")
        except Exception as e:
            print(f"  [Error] Failed to remove {media_dir}: {e}")

    # 3. Clean .agents/ directory
    agents_dir = os.path.join(brain_dir, ".agents")
    if os.path.exists(agents_dir):
        try:
            shutil.rmtree(agents_dir, onerror=remove_readonly)
            print(f"✓ Removed temporary session agents directory: {agents_dir}")
        except Exception as e:
            print(f"  [Error] Failed to remove {agents_dir}: {e}")

    # 4. Clean background task logs in .system_generated/tasks/ (task-*.log only, keep directory & transcripts)
    tasks_log_dir = os.path.join(brain_dir, ".system_generated", "tasks")
    if os.path.exists(tasks_log_dir):
        task_logs = [f for f in os.listdir(tasks_log_dir) if f.startswith("task-") and f.endswith(".log")]
        deleted_logs = 0
        for f in task_logs:
            try:
                os.remove(os.path.join(tasks_log_dir, f))
                deleted_logs += 1
            except Exception:
                pass
        if deleted_logs > 0:
            print(f"✓ Cleared {deleted_logs} background command log(s) from .system_generated/tasks/")

    # 5. Handle root-level files
    preserved_artifacts = []
    deleted_files = []
    
    for item in os.listdir(brain_dir):
        item_path = os.path.join(brain_dir, item)
        if os.path.isdir(item_path):
            continue
        
        ext = os.path.splitext(item)[1].lower()
        
        if clean_artifacts:
            try:
                os.remove(item_path)
                deleted_files.append(item)
            except Exception as e:
                print(f"  [Error] Failed to delete {item}: {e}")
        else:
            if ext == '.md':
                preserved_artifacts.append(item)
            elif ext == '.json' and item.endswith('.metadata.json'):
                md_target = item[:-len('.metadata.json')]
                if not os.path.exists(os.path.join(brain_dir, md_target)):
                    try:
                        os.remove(item_path)
                        deleted_files.append(item)
                    except Exception:
                        pass
                else:
                    preserved_artifacts.append(item)
            elif ext in ['.tmp', '.log', '.bak', '.out']:
                try:
                    os.remove(item_path)
                    deleted_files.append(item)
                except Exception:
                    pass

    if deleted_files:
        print(f"✓ Deleted {len(deleted_files)} root file(s): {', '.join(deleted_files[:5])}{'...' if len(deleted_files) > 5 else ''}")
    if preserved_artifacts:
        print(f"ℹ Preserved {len(preserved_artifacts)} design artifact(s): {', '.join(preserved_artifacts[:5])}{'...' if len(preserved_artifacts) > 5 else ''}")

    print("-" * 50)
    print("Session brain cleanup complete.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Clean temporary files from an Antigravity session's brain directory.")
    parser.add_argument("conversation_id", help="The conversation ID (UUID) of the session to clean.")
    parser.add_argument("--all", "-a", action="store_true", help="Full reset: delete root artifacts (*.md, etc.) as well.")
    
    args = parser.parse_args()
    clean_brain(args.conversation_id, clean_artifacts=args.all)

if __name__ == "__main__":
    main()
