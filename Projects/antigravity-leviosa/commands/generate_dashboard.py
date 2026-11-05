import os
import glob
import json
import re

PROJECT_DIR = os.path.expanduser("~/.gemini/Projects/antigravity-leviosa")
TASKS_DIR = os.path.join(PROJECT_DIR, "tasks")
OUTPUT_HTML = "/Users/kael/.gemini/antigravity/brain/4282f618-0b6a-49c7-a16e-c9884bc4f2c4/project_dashboard.html"

def parse_task(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    parts = content.split('---')
    if len(parts) >= 3:
        frontmatter_text = parts[1]
        
        # simple manual parsing
        title = "Unknown"
        status = "backlog"
        priority = "low"
        tags = []
        
        for line in frontmatter_text.split('\n'):
            line = line.strip()
            if line.startswith('title:'):
                title = line.split(':', 1)[1].strip().strip('"').strip("'")
            elif line.startswith('status:'):
                status = line.split(':', 1)[1].strip().lower()
            elif line.startswith('priority:'):
                priority = line.split(':', 1)[1].strip().lower()
            elif line.startswith('tags:'):
                tags_str = line.split(':', 1)[1].strip()
                tags_str = tags_str.strip('[]')
                tags = [t.strip().strip('"').strip("'") for t in tags_str.split(',') if t.strip()]
                
        return {
            'id': os.path.basename(filepath),
            'title': title,
            'status': status,
            'priority': priority,
            'tags': tags
        }
    return None

def main():
    tasks = []
    if os.path.exists(TASKS_DIR):
        for fp in glob.glob(os.path.join(TASKS_DIR, "*.md")):
            t = parse_task(fp)
            if t:
                tasks.append(t)
    
    backlog = [t for t in tasks if t['status'] == 'backlog']
    active = [t for t in tasks if t['status'] == 'active']
    completed = [t for t in tasks if t['status'] == 'completed']

    def render_column(title, column_tasks):
        html = f"""<div class="flex flex-col gap-3">
          <h3 class="text-xs font-semibold text-[var(--muted-foreground)] uppercase tracking-wider flex items-center gap-2">
            {title} <span class="bg-[var(--border)] text-[var(--foreground)] px-1.5 rounded-full text-[10px]">{len(column_tasks)}</span>
          </h3>"""
        for t in column_tasks:
            color = 'bg-red-500' if t['priority'] == 'high' else 'bg-yellow-500' if t['priority'] == 'medium' else 'bg-blue-500'
            tags_html = "".join([f'<span class="text-[10px] px-1.5 py-0.5 bg-[var(--border)] rounded text-[var(--muted-foreground)]">{tag}</span>' for tag in t['tags']])
            
            html += f"""
          <div class="bg-[var(--card)] border border-[var(--border)] rounded-lg p-3 hover:border-[var(--primary)] cursor-pointer transition-colors shadow-sm">
            <div class="flex justify-between items-start mb-2">
              <span class="text-[10px] font-mono text-[var(--muted-foreground)]">{t['id']}</span>
              <span class="w-2 h-2 rounded-full {color}" title="{t['priority'].capitalize()} Priority"></span>
            </div>
            <h4 class="text-sm font-medium mb-2">{t['title']}</h4>
            <div class="flex gap-1 flex-wrap">{tags_html}</div>
          </div>"""
        html += "</div>"
        return html

    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 10px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: var(--muted-foreground); }}
  </style>
</head>
<body class="bg-transparent text-[var(--foreground)] antialiased p-4">
  <div class="bg-[var(--background)] text-[var(--foreground)] border border-[var(--border)] rounded-xl h-[600px] flex flex-col shadow-lg overflow-hidden">
    
    <!-- Header -->
    <div class="border-b border-[var(--border)] p-4 flex justify-between items-center bg-[var(--card)]">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded bg-[var(--primary)] text-[var(--primary-foreground)] flex items-center justify-center font-bold">PM</div>
        <div>
          <h1 class="font-semibold text-lg leading-tight">Live Project Dashboard</h1>
          <p class="text-[var(--muted-foreground)] text-xs">Data sourced directly from ~/.gemini/Projects/antigravity-leviosa/tasks/</p>
        </div>
      </div>
      <div class="flex gap-2">
        <span class="px-2 py-1 bg-green-500/10 text-green-500 text-xs rounded border border-green-500/20">Git: Clean</span>
        <span class="px-2 py-1 bg-blue-500/10 text-blue-500 text-xs rounded border border-blue-500/20">PVE-Native</span>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="flex border-b border-[var(--border)] bg-[var(--card)] text-sm">
      <button class="px-4 py-2 border-b-2 border-[var(--primary)] text-[var(--foreground)] font-medium">Tasks Kanban</button>
      <button class="px-4 py-2 border-b-2 border-transparent text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors">Knowledge Base</button>
      <button class="px-4 py-2 border-b-2 border-transparent text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors">Conversations</button>
    </div>

    <!-- Main Content Area: Kanban -->
    <div class="flex-1 overflow-y-auto p-4 bg-[var(--background)]">
      <div class="grid grid-cols-3 gap-4 h-full">
        {render_column('Backlog', backlog)}
        {render_column('Active', active)}
        {render_column('Completed', completed)}
      </div>
    </div>
  </div>
</body>
</html>"""

    with open(OUTPUT_HTML, "w") as f:
        f.write(html_content)
    print("Dashboard generated successfully.")

if __name__ == "__main__":
    main()
