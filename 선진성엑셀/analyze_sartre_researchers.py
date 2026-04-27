import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

file_path = r"C:\Users\User\Desktop\선진성엑셀\KCI_excel_202612163364.xls"
df = pd.read_excel(file_path, engine='xlrd')

keywords_series = df['저자키워드'].dropna()

people_mapping = {
    "사르트르": ["사르트르", "장 폴 사르트르", "장-폴 사르트르", "장폴 사르트르", "사르트르(sartre)", "사르트르sartre", "sartre", "jean-paul sartre", "jean paul sartre"],
    "하이데거": ["하이데거", "마르틴 하이데거", "마르틴하이데거", "heidegger"],
    "메를로-퐁티": ["메를로-퐁티", "메를로 퐁티", "메를로퐁티", "모리스 메를로-퐁티", "merleau-ponty"],
    "카뮈": ["카뮈", "알베르 카뮈", "까뮈", "알베르 까뮈", "camus", "albert camus"],
    "들뢰즈": ["들뢰즈", "질 들뢰즈", "들뢰즈(g. deleuze)", "질들뢰즈", "deleuze", "gilles deleuze"],
    "보부아르": ["보부아르", "시몬 드 보부아르", "시몬 보부아르", "beauvoir", "simone de beauvoir"],
    "니체": ["니체", "프리드리히 니체", "nietzsche"],
    "마르크스": ["마르크스", "칼 마르크스", "카를 마르크스", "맑스", "marx"],
    "헤겔": ["헤겔", "g. w. f. 헤겔", "hegel"],
    "레비나스": ["레비나스", "에마뉘엘 레비나스", "엠마누엘 레비나스", "levinas"],
    "후설": ["후설", "에드문트 후설", "husserl"],
    "바디우": ["바디우", "알랭 바디우", "badiou"],
    "키르케고르": ["키르케고르", "쇠렌 키르케고르", "키에르케고어", "kierkegaard"],
    "아렌트": ["아렌트", "한나 아렌트", "한나아렌트", "arendt"],
    "푸코": ["푸코", "미셸 푸코", "미셀 푸코", "foucault"],
    "라캉": ["라캉", "자크 라캉", "lacan"],
    "데카르트": ["데카르트", "르네 데카르트", "descartes"]
}

# 역순 매핑 딕셔너리 생성 (검색 속도 향상을 위해)
reverse_mapping = {}
for canonical, aliases in people_mapping.items():
    for alias in aliases:
        reverse_mapping[alias.lower()] = canonical

people_counts = {}

for kws in keywords_series:
    parts = kws.split(',')
    for part in parts:
        clean_kw = part.strip().lower() # 소문자로 변환해서 비교
        if clean_kw in reverse_mapping:
            canonical_name = reverse_mapping[clean_kw]
            people_counts[canonical_name] = people_counts.get(canonical_name, 0) + 1

# 결과 Series 변환 후 정렬
s_people = pd.Series(people_counts).sort_values(ascending=False)

# 상위 15명 추출 (사람 수가 15명 미만일 수 있으니 헤드는 15로 제한)
top_people = s_people.head(15).copy()

# 가로 막대 그래프 그리기 (상위가 위로 오도록 역순 정렬)
top_people = top_people[::-1]

plt.figure(figsize=(10, 8))
bars = plt.barh(top_people.index, top_people.values, color='cornflowerblue', edgecolor='black')

# 막대 옆에 숫자 표시
for bar in bars:
    width = bar.get_width()
    plt.text(width + width*0.01, bar.get_y() + bar.get_height()/2, 
             f'{int(width)}', 
             ha='left', va='center', fontsize=10)

plt.title('이 엑셀파일에서 언급된 실존주의 철학자들의 빈도수', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('언급 빈도수', fontsize=12)
plt.ylabel('연구자 (학자)', fontsize=12)
plt.xlim(0, max(top_people.values) * 1.1)
plt.tight_layout()

# 그래프 저장
output_path = r"C:\Users\User\Desktop\선진성엑셀\실존주의_연구자_언급빈도.png"
plt.savefig(output_path, dpi=300)

print(f"상위 연구자 언급 빈도 분석 완료. 그래프가 {output_path} 에 저장되었습니다.")
for k, v in top_people[::-1].items():
    print(f"{k}: {v}")
