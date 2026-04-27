import pandas as pd
import matplotlib.pyplot as plt
import sys

# Windows에서 한국어 폰트 설정 (맑은 고딕)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# Excel 파일 읽기
file_path = r"C:\Users\User\Desktop\선진성엑셀\KCI_excel_202612163364.xls"
df = pd.read_excel(file_path, engine='xlrd')

# 연도별 데이터 수 계산
yearly_counts = df['발행연도'].value_counts().sort_index()

# 2023년 데이터 수 파악
count_2023 = yearly_counts.get(2023, 0)
print(f"2023년도 데이터 개수: {count_2023}개")
print(f"전체 평균 건수: {yearly_counts.mean():.1f}개")

# 그래프 생성
plt.figure(figsize=(10, 6))

# 연도를 문자열로 변환하여 x축으로 사용
years = yearly_counts.index.astype(str)
counts = yearly_counts.values

# 바 차트 그리기
bars = plt.bar(years, counts, color='lightgray', edgecolor='black')

# 2023년 막대 강조
for i, year in enumerate(yearly_counts.index):
    if year == 2023:
        bars[i].set_color('salmon')
        bars[i].set_edgecolor('black')
    
    # 막대 위에 숫자 표시
    plt.text(i, counts[i] + max(counts)*0.01, str(counts[i]), ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.title('연도별 논문 발행 건수', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('발행연도', fontsize=12)
plt.ylabel('발행 건수', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# 그래프를 이미지로 저장
output_path = r"C:\Users\User\Desktop\선진성엑셀\yearly_chart.png"
plt.savefig(output_path, dpi=300)
print(f"그래프 저장 완료: {output_path}")
