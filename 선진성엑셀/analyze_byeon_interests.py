import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter

# Windows 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

file_path = r"C:\Users\User\Desktop\선진성엑셀\KCI_excel_202612163364.xls"
df = pd.read_excel(file_path, engine='xlrd')

# '변광배' 저자 필터링
byeon_df = df[df['저자명'].fillna('').str.contains('변광배')].copy()

# 불용어(Stop words) 목록 정의 (의미 없는 단어 제거)
stop_words = {
    '통한', '대한', '연구', '고찰', '중심으로', '비교', '관한', '분석', '이해', '사상', '이론', '문제', '개념', '철학', '위한', '그리고', '나타난', '사르트르의', '사르트르와', '메를로', '존재와', '읽기', '또는', '대하여', '대해', 'la', 'de', 'le', 'et', 'les', 'des', 'du', 'en', 'un', 'une', '그', '와', '과', '에서', '를', '은', '는', '이', '가', '에', '적', '성', '적용', '방안', '사르트르', '장 폴 사르트르', 'sartre', '장폴', '현상학적', '프랑스', 'jean-paul sartre', 'jean-paul', '의미', '비판', '관점'
}

all_words = []
paper_words_list = []

for _, row in byeon_df.iterrows():
    p_words = set()
    
    # 1. 저자키워드에서 추출
    if pd.notna(row['저자키워드']):
        kws = [k.strip().lower() for k in re.split(r'[,;]', str(row['저자키워드'])) if k.strip()]
        for k in kws:
            if k not in stop_words and len(k) > 1:
                p_words.add(k)
                
    # 2. 논문명에서 추가 추출 (특수문자 제거 후 단어 단위)
    title = str(row['논문명']) if pd.notna(row['논문명']) else ""
    title_words = [re.sub(r'[^\w\s\uac00-\ud7a3a-zA-Z]', '', w.lower()) for w in title.split()]
    for tw in title_words:
        if len(tw) > 1 and tw not in stop_words:
            p_words.add(tw)
            
    paper_words_list.append(list(p_words))
    all_words.extend(list(p_words))

word_counts = Counter(all_words)

# 빈도수 높은 상위 5개 관심사 단어 추출
top_5_keywords = [w[0] for w in word_counts.most_common(5)]

# 연도별 트렌드 데이터프레임
years = sorted(byeon_df['발행연도'].dropna().astype(int).unique())
full_years = list(range(min(years), max(years)+1)) if years else []
trend_df = pd.DataFrame(0, index=full_years, columns=top_5_keywords)

for year, p_words in zip(byeon_df['발행연도'], paper_words_list):
    if pd.isna(year): continue
    year = int(year)
    for tw in top_5_keywords:
        if tw in p_words:
            trend_df.at[year, tw] += 1

# 다중 라인 그래프 시각화
plt.figure(figsize=(12, 7))

colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00']
markers = ['o', 's', '^', 'D', 'v']

for i, tw in enumerate(top_5_keywords):
    plt.plot(trend_df.index.astype(str), trend_df[tw], marker=markers[i], color=colors[i], linewidth=2.5, markersize=8, label=tw)

plt.title('변광배 연구자의 주요 관심사(키워드) 연도별 변화 추이', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('발행연도', fontsize=12)
plt.ylabel('관련 논문 게재 수 (건)', fontsize=12)
plt.xticks(rotation=45)

max_y = trend_df.max().max() if not trend_df.empty else 5
plt.ylim(0, max_y + 1)
plt.yticks(range(0, int(max_y) + 2))
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title='주요 키워드 (Top 5)', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10, title_fontsize=12)
plt.tight_layout()

# 이미지 저장
output_path = r"C:\Users\User\Desktop\선진성엑셀\byeon_interests_trend.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')

# 텍스트 결과 저장
with open(r"C:\Users\User\Desktop\선진성엑셀\byeon_interests_output.txt", "w", encoding="utf-8") as f:
    f.write("==== 변광배 연구자 세부 핵심 키워드 Top 5 ====\n")
    for tw in top_5_keywords:
        f.write(f"- {tw}: {word_counts[tw]}건\n")

print(f"변광배 관심사 추이 시각화 완료: {output_path}")
