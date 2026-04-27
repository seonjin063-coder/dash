import pandas as pd
import matplotlib.pyplot as plt

# Windows에서 한국어 폰트 설정 (맑은 고딕)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# Excel 파일 읽기
file_path = r"C:\Users\User\Desktop\선진성엑셀\KCI_excel_202612163364.xls"
df = pd.read_excel(file_path, engine='xlrd')

# '저자키워드' 결측치 처리
keywords_series = df['저자키워드'].dropna()

# 키워드 분리 및 정제
all_keywords = []
for kws in keywords_series:
    # 콤마로 분리
    parts = kws.split(',')
    for part in parts:
        clean_kw = part.strip()
        if clean_kw:
            # 영어인 경우 소문자로 통일할 수도 있지만, 우선 형태 그대로 유지
            all_keywords.append(clean_kw)

# 빈도수 계산
keyword_counts = pd.Series(all_keywords).value_counts()

# 상위 15개 추출
top_15_keywords = keyword_counts.head(15)

# 가로 막대 그래프 그리기 (상위가 위로 오도록 역순 정렬)
top_15_keywords = top_15_keywords[::-1]

plt.figure(figsize=(10, 8))
bars = plt.barh(top_15_keywords.index, top_15_keywords.values, color='skyblue', edgecolor='black')

# 막대 옆에 숫자 표시
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.3, bar.get_y() + bar.get_height()/2, 
             f'{int(width)}', 
             ha='left', va='center', fontsize=10)

plt.title('사르트르 연구의 주요 키워드 (kci)', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('빈도수', fontsize=12)
plt.ylabel('키워드', fontsize=12)
plt.tight_layout()

# 그래프 저장
output_path = r"C:\Users\User\Desktop\선진성엑셀\사르트르_주요키워드.png"
plt.savefig(output_path, dpi=300)

print(f"상위 15개 키워드 분석 완료. 그래프가 {output_path} 에 저장되었습니다.")
for k, v in top_15_keywords[::-1].items():
    print(f"{k}: {v}")
