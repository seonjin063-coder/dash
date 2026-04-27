import pandas as pd
import matplotlib.pyplot as plt

# Windows에서 한국어 폰트 설정 (맑은 고딕)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# Excel 파일 읽기
file_path = r"C:\Users\User\Desktop\선진성엑셀\KCI_excel_202612163364.xls"
df = pd.read_excel(file_path, engine='xlrd')

# 연도별 데이터 수 계산 (결측치 제거 후 정수형 변환)
yearly_counts = df['발행연도'].dropna().astype(int).value_counts().sort_index()

# 가장 논문이 많이 발표된 해 찾기
max_year = yearly_counts.idxmax()
max_count = yearly_counts.max()
print(f"가장 많은 논문이 발표된 해: {max_year}년 ({max_count}건)")

# 그래프 생성 (라인 그래프)
plt.figure(figsize=(12, 6))

# 연도를 문자열로 변환하여 x축으로 사용
years = yearly_counts.index.astype(str)
counts = yearly_counts.values

# 라인 그래프 그리기 (마커 포함)
plt.plot(years, counts, marker='o', linestyle='-', color='#1f77b4', linewidth=2, markersize=6)

# 최대값 포인트 표시
max_index = list(years).index(str(max_year))
plt.plot(max_index, max_count, marker='o', color='red', markersize=10, label=f'최대 발행: {max_year}년 ({max_count}건)')
plt.legend()

# 각 포인트 위에 숫자 표시
for i, count in enumerate(counts):
    plt.annotate(str(count), 
                 xy=(i, count), 
                 xytext=(0, 8), 
                 textcoords='offset points', 
                 ha='center', 
                 va='bottom', 
                 fontsize=10)

plt.title('연도별 전체 논문 발행 추이', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('발행연도', fontsize=12)
plt.ylabel('발행 건수', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)

# 상단 여백 확보
plt.ylim(0, max_count * 1.15)
plt.tight_layout()

# 그래프를 이미지로 저장
output_path = r"C:\Users\User\Desktop\선진성엑셀\yearly_trend_line.png"
plt.savefig(output_path, dpi=300)
print(f"그래프 저장 완료: {output_path}")
