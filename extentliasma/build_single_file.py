import json
import os

base_dir = r"c:\Users\User\Desktop\진성이의 실존주의"

# Read components
with open(os.path.join(base_dir, "web", "index.html"), "r", encoding="utf-8") as f:
    html = f.read()

with open(os.path.join(base_dir, "web", "style.css"), "r", encoding="utf-8") as f:
    css = f.read()

with open(os.path.join(base_dir, "web", "app.js"), "r", encoding="utf-8") as f:
    js = f.read()

with open(os.path.join(base_dir, "output", "dashboard_data.json"), "r", encoding="utf-8") as f:
    data_json = f.read()

# Replace css link with inline style
html = html.replace('<link rel="stylesheet" href="style.css">', f'<style>\n{css}\n</style>')

# Modifying JS to use embedded data instead of fetch
js = js.replace("fetch('../output/dashboard_data.json')", f"Promise.resolve({{ ok: true, json: () => Promise.resolve({data_json}) }})")

# Replace js script src with inline script
html = html.replace('<script src="app.js"></script>', f'<script>\n{js}\n</script>')

output_path = r"c:\Users\User\Desktop\실존주의_대시보드.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Portable dashboard successfully created at: {output_path}")
