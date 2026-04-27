import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter

# Windows에서 한국어 폰트 설정 (맑은 고딕)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# Excel 파일 읽기
file_path = r"C:\Users\User\Desktop\선진성엑셀\KCI_excel_202612163364.xls"
df = pd.read_excel(file_path, engine='xlrd')

# 저자키워드 정제 함수
def clean_keyword(text):
    if pd.isna(text):
        return ""
    # 특수문자 제거 후 띄어쓰기 기준으로 처리할 수도 있으나, 키워드는 전체 형태를 유지 (소문자 변환만)
    return str(text).lower()

# 키워드 추출
keyword_col = '저자키워드'
all_keywords = []

if keyword_col in df.columns:
    col_data = df[keyword_col].dropna().astype(str)
    for row in col_data:
        # , 와 ; 로 키워드 분리
        words = [word.strip() for word in re.split(r'[,;]', row)]
        # 특수문자 제거 및 소문자화
        cleaned_words = [re.sub(r'[^\w\s\u3131-\u3163\uac00-\ud7a3]', '', w.lower()).strip() for w in words]
        all_keywords.extend([w for w in cleaned_words if w]) # 빈 문자열 제외

# 빈도수 계산
keyword_counts = Counter(all_keywords)

# 상위 15개 추출
top15_keywords = keyword_counts.most_common(15)

# 파일로 상위 15개 텍스트 저장
with open(r"C:\Users\User\Desktop\선진성엑셀\top15_keywords_output.txt", "w", encoding="utf-8") as f:
    f.write("==== 저자키워드 상위 15개 ====\n")
    for idx, (kw, cnt) in enumerate(top15_keywords):
        f.write(f"{idx+1}. {kw} : {cnt}건\n")

# 시각화할 키워드 선택 (가장 많이 나오는 '사르트르'는 너무 포괄적이므로 두 번째 또는 의미있는 키워드 선택)
# 여기서는 2위에 해당하는 키워드를 선택하도록 합니다 (보통 '실존주의'나 '자유').
target_keyword = top15_keywords[1][0] if len(top15_keywords) > 1 else top15_keywords[0][0]
if target_keyword == '사르트르' and len(top15_keywords) > 2:
    target_keyword = top15_keywords[2][0]

print(f"선택된 분석 대상 키워드: '{target_keyword}'")

# 선택 키워드가 포함된 논문 필터링 (결측치 제외)
# 정확히 해당 키워드를 포함하는 경우가 더 정확하지만, 여기서는 부분일치 허용 혹은 키워드 리스트로 필터
df['저자키워드'] = df['저자키워드'].fillna('')
# 정규표현식 이스케이프 필요할 수 있으나 일반적인 단어면 문제없음
kw_df = df[df['저자키워드'].str.contains(target_keyword, case=False, na=False)]

# 연도별 데이터 수 계산 (결측치 제거 후 정수형 변환)
yearly_counts = kw_df['발행연도'].dropna().astype(int).value_counts().sort_index()

# 라인 그래프 생성
plt.figure(figsize=(10, 6))

# 연도를 문자열로 변환하여 x축으로 사용
years = yearly_counts.index.astype(str)
counts = yearly_counts.values

# 라인 그래프 그리기 (마커 포함)
plt.plot(years, counts, marker='o', linestyle='-', color='#2ca02c', linewidth=2.5, markersize=8)

# 그래프 꾸미기
for i, count in enumerate(counts):
    plt.annotate(str(count), 
                 xy=(i, count), 
                 xytext=(0, 10), 
                 textcoords='offset points', 
                 ha='center', 
                 va='bottom', 
                 fontsize=11)

plt.title(f"연도별 '{target_keyword}' 키워드 포함 논문 발행 추이", fontsize=16, fontweight='bold', pad=15)
plt.xlabel('발행연도', fontsize=12)
plt.ylabel('발행 건수', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)

# 상단 여백 확보
if len(counts) > 0:
    plt.ylim(0, max(counts) * 1.2)

plt.tight_layout()

# 그래프를 이미지로 저장
output_path = r"C:\Users\User\Desktop\선진성엑셀\keyword_trend_line.png"
plt.savefig(output_path, dpi=300)
print(f"그래프 저장 완료: {output_path}")

with open(r"C:\Users\User\Desktop\선진성엑셀\top15_keywords_output.txt", "a", encoding="utf-8") as f:
    f.write(f"\n=> 선택된 키워드 '{target_keyword}'에 대한 연도별 추이 그래프를 생성했습니다.\n")
