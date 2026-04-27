import pandas as pd
from collections import Counter
import re
import sys

# Excel 파일 읽기
file_path = r"C:\Users\User\Desktop\선진성엑셀\KCI_excel_202612163364.xls"
df = pd.read_excel(file_path, engine='xlrd')

# 텍스트 정제 함수
def clean_text(text):
    if pd.isna(text):
        return ""
    # 특수문자 제거 및 소문자 변환
    text = re.sub(r'[^\w\s\u3131-\u3163\uac00-\ud7a3]', ' ', str(text).lower())
    return text

# 주제어 추출
titles = ' '.join(df['논문명'].apply(clean_text)).split()

# 의미 없는 불용어 제거
stop_words = set(['및', '대한', '연구', '고찰', '중심으로', '통한', '의미', '비교', '관한', '분석', '이해', '사상', '이론', '문제', '개념', '철학', '위한', '그', '와', '과', '에서', '를', '은', '는', '이', '가', '에', '적', '성', '적용', '방안'])
filtered_titles = [word for word in titles if len(word) > 1 and word not in stop_words]

title_counts = Counter(filtered_titles).most_common(20)

with open(r"C:\Users\User\Desktop\선진성엑셀\theme_output.txt", "w", encoding="utf-8") as f:
    f.write(f"총 논문 건수: {len(df)}\n")
    f.write("==== 전체 논문 주요 단어 빈도 (논문명 기준) ====\n")
    for word, count in title_counts:
        f.write(f"- {word}: {count}번\n")

    # 저자 키워드 혹은 한국어 키워드 컬럼이 있다면 확인
    keyword_cols = [col for col in df.columns if '키워드' in col or '주제어' in col]
    if keyword_cols:
        keywords = []
        for col in keyword_cols:
            col_data = df[col].dropna().astype(str)
            for row in col_data:
                words = [word.strip() for word in re.split(r'[,;]', row)]
                keywords.extend([clean_text(w) for w in words if w])
                
        filtered_keywords = [word for word in keywords if len(word) > 1 and word not in stop_words]
        keyword_counts = Counter(filtered_keywords).most_common(20)
        
        f.write("\n==== 전체 논문 주요 단어 빈도 (키워드/주제어 기준) ====\n")
        for word, count in keyword_counts:
            f.write(f"- {word}: {count}번\n")
    else:
        f.write("\n키워드(주제어) 컬럼을 찾을 수 없습니다.\n")

    f.write("\n컬럼 목록:\n")
    f.write(", ".join(df.columns) + "\n")
