import pandas as pd

file_path = r"C:\Users\User\Desktop\선진성엑셀\KCI_excel_202612163364.xls"
df = pd.read_excel(file_path, engine='xlrd')
keywords_series = df['저자키워드'].dropna()

all_keywords = []
for kws in keywords_series:
    parts = kws.split(',')
    for part in parts:
        clean_kw = part.strip()
        if clean_kw:
            all_keywords.append(clean_kw)

keyword_counts = pd.Series(all_keywords).value_counts()
print(keyword_counts.head(50).to_string())
