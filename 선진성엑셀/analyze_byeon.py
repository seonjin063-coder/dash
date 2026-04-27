import pandas as pd
import matplotlib.pyplot as plt
import re

# Windows에서 한국어 폰트 설정 (맑은 고딕)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# Excel 파일 읽기
file_path = r"C:\Users\User\Desktop\선진성엑셀\KCI_excel_202612163364.xls"
df = pd.read_excel(file_path, engine='xlrd')

# '변광배' 저자가 포함된 데이터 필터링
# 결측치 처리
df['저자명'] = df['저자명'].fillna('')
byeon_df = df[df['저자명'].str.contains('변광배')]

# 학술지별 논문 발표 건수 계산
journal_counts = byeon_df['학술지명'].value_counts()

# 파이차트 생성
plt.figure(figsize=(12, 9))

# 디자인을 위한 색상 팔레트 설정
colors = plt.cm.Set3.colors

# 파이차트 그리기
# 학술지가 너무 많을 수 있으니, 경우에 따라 상위 N개만 표시하거나 기타로 묶는 것이 좋지만
# 일단 전체를 다 그리고, 너무 비율이 작은 건 합칠 수 있습니다.
# 전체 28건이므로 종류가 그렇게 많지 않을 수 있습니다.
wedges, texts, autotexts = plt.pie(
    journal_counts, 
    labels=journal_counts.index, 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=colors,
    wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
    textprops={'fontsize': 10}
)

# 퍼센트 텍스트 스타일 변경
for autotext in autotexts:
    autotext.set_fontweight('bold')

plt.title('변광배 연구자의 학술지별 논문 발표 비율', fontsize=16, fontweight='bold', pad=20)
plt.axis('equal') # 원형으로 보이게 설정
plt.tight_layout()

# 그래프를 이미지로 저장
output_path = r"C:\Users\User\Desktop\선진성엑셀\byeon_journals_pie_chart.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')

# 파일로 출력 내용 저장
with open(r"C:\Users\User\Desktop\선진성엑셀\byeon_journals_output.txt", "w", encoding="utf-8") as f:
    f.write(f"변광배 연구자 총 발행 건수: {len(byeon_df)}\n")
    for journal, count in journal_counts.items():
        f.write(f"- {journal}: {count}건\n")

print(f"파이차트 저장 완료: {output_path}")
