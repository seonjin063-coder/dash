import pandas as pd
import re

file_path = r"C:\Users\User\Desktop\선진성엑셀\KCI_excel_202612163364.xls"
df = pd.read_excel(file_path, engine='xlrd')

authors_series = df['저자명'].dropna().astype(str)
all_authors = []
for authors_str in authors_series:
    authors = [a.strip() for a in re.split(r'[,;]', authors_str) if a.strip()]
    all_authors.extend(authors)

author_counts = pd.Series(all_authors).value_counts().head(10)

with open(r"C:\Users\User\Desktop\선진성엑셀\authors_output.txt", "w", encoding="utf-8") as f:
    for author, count in author_counts.items():
        f.write(f"{author}: {count}건\n")
