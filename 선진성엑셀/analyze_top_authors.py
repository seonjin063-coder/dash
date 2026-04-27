import pandas as pd
import matplotlib.pyplot as plt
import re

# Windows에서 한국어 폰트 설정 (맑은 고딕)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# Excel 파일 읽기
file_path = r"C:\Users\User\Desktop\선진성엑셀\KCI_excel_202612163364.xls"
df = pd.read_excel(file_path, engine='xlrd')

# 저자명 데이터 전처리 및 분리
authors_series = df['저자명'].dropna().astype(str)
all_authors = []
for authors_str in authors_series:
    # 쉼표나 세미콜론으로 여러 저자가 구분되는 경우 분리
    authors = [a.strip() for a in re.split(r'[,;]', authors_str) if a.strip()]
    all_authors.extend(authors)

# 빈도수 계산
author_counts = pd.Series(all_authors).value_counts()

# 상위 10명 추출
top10_authors = author_counts.head(10)

# 파이차트 생성
plt.figure(figsize=(10, 8))

# 디자인을 위한 색상 팔레트 설정
colors = plt.cm.Set3.colors

# 파이차트 그리기
wedges, texts, autotexts = plt.pie(
    top10_authors, 
    labels=top10_authors.index, 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=colors,
    wedgeprops={'edgecolor': 'white', 'linewidth': 2},
    textprops={'fontsize': 11}
)

# 퍼센트 텍스트 스타일 변경
for autotext in autotexts:
    autotext.set_fontweight('bold')

plt.title('상위 10명 연구자 논문 발표 비율 (Top 10)', fontsize=16, fontweight='bold', pad=20)
plt.axis('equal') # 원형으로 보이게 설정
plt.tight_layout()

# 그래프를 이미지로 저장
output_path = r"C:\Users\User\Desktop\선진성엑셀\top10_authors_pie_chart.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')

print("상위 10명 연구자:")
for author, count in top10_authors.items():
    print(f"- {author}: {count}건")
print(f"\n파이차트가 저장되었습니다: {output_path}")
