import pandas as pd
import json
import os
import glob
from itertools import combinations
from collections import Counter

def load_kci_data(downloads_path):
    # 다양한 경로에서 파일 찾기
    search_paths = [
        os.path.join(downloads_path, '*.xls'), 
        os.path.join(downloads_path, '*.csv'),
        './*.xls', './*.csv'
    ]
    files = []
    for path in search_paths:
        files.extend(glob.glob(path))
        
    if not files:
        # 상위 폴더도 확인
        files = glob.glob('../downloads/*.xls') or glob.glob('../*.xls')
        if not files:
            print("[오류] 데이터를 찾을 수 없습니다. downloads 폴더를 확인하세요.")
            return None
        
    file_path = files[0]
    print(f"[{os.path.basename(file_path)}] 데이터를 불러오는 중...")
    
    try:
        if file_path.endswith('.xls'):
            try:
                # KCI HTML 엑셀인 경우
                dfs = pd.read_html(file_path, encoding='utf-8')
                df = dfs[0]
            except Exception:
                # 일반 엑셀
                df = pd.read_excel(file_path)
        else:
            try:
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file_path, encoding='cp949')
                
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        print(f"[오류] 데이터 읽기 실패: {e}")
        return None

def process_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    downloads_path = os.path.join(base_dir, '..', 'downloads')
    output_path = os.path.join(base_dir, '..', 'output')
    
    df = load_kci_data(downloads_path)
    if df is None:
        return

    # ----- 1. 영향력 랭킹 (Focus Gauge) -----
    print("(1/3) 영향력 랭킹 분석 중...")
    df['인용된 총 횟수'] = pd.to_numeric(df['인용된 총 횟수'], errors='coerce').fillna(0)
    top_papers = df.sort_values(by='인용된 총 횟수', ascending=False).head(10)
    
    focus_gauge_data = []
    for _, row in top_papers.iterrows():
        focus_gauge_data.append({
            "title": str(row['논문명']) if pd.notna(row.get('논문명')) else '제목 없음',
            "author": str(row['저자명']) if pd.notna(row.get('저자명')) else '저자 미상',
            "citations": int(row['인용된 총 횟수']),
            "year": int(row['발행연도']) if pd.notna(row.get('발행연도')) else None,
            "journal": str(row['학술지명']) if pd.notna(row.get('학술지명')) else '학술지 미상'
        })

    # ----- 2. 연도별 연구 밀도 (Timeline) -----
    print("(2/3) 연도별 논문 발행량 분석 중...")
    df['발행연도'] = pd.to_numeric(df['발행연도'], errors='coerce')
    timeline_df = df.dropna(subset=['발행연도'])
    timeline_counts = timeline_df['발행연도'].value_counts().sort_index()
    
    timeline_data = [
        {"year": int(year), "count": int(count)}
        for year, count in timeline_counts.items()
    ]

    # ----- 3. 자유-키워드 네트워크 (Navigation Map) -----
    print("(3/3) 키워드 연결망 구축 중...")
    df_keywords = df['저자키워드'].dropna().astype(str)
    
    keyword_freq = Counter()
    edges_counter = Counter()
    
    for keywords_str in df_keywords:
        # 단어 자르기
        kws = [k.strip() for k in keywords_str.split(',') if k.strip()]
        if kws:
            keyword_freq.update(kws)
            # 단어들끼리의 동시출현 연결(Edge) 생성
            for w1, w2 in combinations(sorted(kws), 2):
                edges_counter[(w1, w2)] += 1

    # 그래프 품질을 위해 핵심 노드 상위 50개만 추출
    top_keywords = dict(keyword_freq.most_common(50))
    
    # GEMINI.md 기획안 필수 키워드 누락 방지 ('자유', '사르트르' 등 주요 키워드 보장)
    essential_kws = ['자유', '사르트르', '실존주의']
    for kw in essential_kws:
        if kw in keyword_freq and kw not in top_keywords:
            top_keywords[kw] = keyword_freq[kw]

    valid_nodes = set(top_keywords.keys())
    
    nodes_data = [{"id": k, "name": k, "value": v} for k, v in top_keywords.items()]
    
    edges_data = []
    for (w1, w2), weight in edges_counter.items():
        if w1 in valid_nodes and w2 in valid_nodes:
            edges_data.append({
                "source": w1,
                "target": w2,
                "value": weight
            })

    # JSON 데이터 최종 병합
    dashboard_data = {
        "focus_gauge": focus_gauge_data,
        "timeline": timeline_data,
        "network": {
            "nodes": nodes_data,
            "links": edges_data
        }
    }

    # JSON 파일로 저장
    os.makedirs(output_path, exist_ok=True)
    out_file = os.path.join(output_path, 'dashboard_data.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, ensure_ascii=False, indent=4)
        
    print(f"\n[성공] 가공된 대시보드 데이터가 저장되었습니다: {out_file}")

if __name__ == '__main__':
    process_data()
