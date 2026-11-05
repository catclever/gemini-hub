#!/usr/bin/env python3
import os
import json
import sys
from glob import glob
from urllib.parse import unquote

def get_meta_dir(current_path):
    projects_dir = os.path.expanduser("~/.gemini/config/projects")
    
    mappings = {}
    for json_file in glob(os.path.join(projects_dir, "*.json")):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                name = data.get("name")
                resources = data.get("projectResources", {}).get("resources", [])
                for res in resources:
                    uri = res.get("gitFolder", {}).get("folderUri", "")
                    if uri.startswith("file://"):
                        path = unquote(uri[7:])
                        mappings[path] = name
        except Exception:
            continue

    curr = os.path.abspath(current_path)
    while curr != "/":
        if curr in mappings:
            return os.path.expanduser(f"~/.gemini/Projects/{mappings[curr]}")
        curr = os.path.dirname(curr)
        
    return ""

if __name__ == "__main__":
    pwd = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    result = get_meta_dir(pwd)
    if result:
        print(result)
        sys.exit(0)
    else:
        sys.exit(1)
