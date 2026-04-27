import pandas as pd

file_path = r"C:\Users\User\Desktop\선진성엑셀\KCI_excel_202612163364.xls"
df = pd.read_excel(file_path, engine='xlrd')
print(df['키워드'].dropna().head(10).tolist())
