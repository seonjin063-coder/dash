import json
import os
import re

base_dir = r'c:\Users\User\Desktop\진성이의 실존주의'
with open(os.path.join(base_dir, 'web', 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()
with open(os.path.join(base_dir, 'web', 'style.css'), 'r', encoding='utf-8') as f:
    css = f.read()
with open(os.path.join(base_dir, 'web', 'app.js'), 'r', encoding='utf-8') as f:
    js = f.read()
with open(os.path.join(base_dir, 'output', 'dashboard_data.json'), 'r', encoding='utf-8') as f:
    data = f.read()

# Replace css link
html = html.replace('<link rel="stylesheet" href="style.css">', f'<style>\n{css}\n</style>')

# Replace fetch
js_safe = js.replace("fetch('../output/dashboard_data.json')", f"Promise.resolve({{ok:true, json: () => Promise.resolve({data})}})")

html = html.replace('<script src="app.js"></script>', f'<script>\n{js_safe}\n</script>')

out_path = r'c:\Users\User\Desktop\진성이의 실존주의 사이트 (논문용).html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Successfully created {out_path}")
