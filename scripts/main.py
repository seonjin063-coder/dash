import pandas as pd
import os
import glob

def load_data():
    # 엑셀 파일이 옮겨지지 않았을 수 있으니 현재 폴더와 downloads 폴더 모두 확인합니다.
    search_paths = ['./*.xls', './*.csv', './downloads/*.xls', './downloads/*.csv']
    files = []
    for path in search_paths:
        files.extend(glob.glob(path))
    
    if not files:
        print("[오류] KCI 데이터를 찾을 수 없습니다!")
        return None
    
    # 첫 번째 파일 선택
    file_path = files[0]
    print(f"[{os.path.basename(file_path)}] 데이터를 읽어옵니다...")
    
    try:
        # KCI에서 다운로드한 .xls 파일은 사실 웹 형식(HTML 표)인 경우가 있습니다.
        if file_path.endswith('.xls'):
            try:
                # KCI HTML 엑셀인 경우
                dfs = pd.read_html(file_path, encoding='utf-8')
                df = dfs[0]
            except Exception:
                # 그냥 평범한 엑셀인 경우
                df = pd.read_excel(file_path)
        else:
            try:
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file_path, encoding='cp949')
    except Exception as e:
         print(f"[오류] 데이터 읽기 실패: {e}")
         return None
         
    return df

# --- 분석 시작 ---
print("===== Antigravity 분석 시작 =====")
df = load_data()

if df is not None:
    print("\n[성공] 데이터를 성공적으로 불러왔습니다!")
    
    # KCI 데이터 컬럼 이름에 숨은 공백이 있을 수 있어 제거
    df.columns = df.columns.str.strip()
    
    # 피인용 수 상위 5개 논문 출력
    if '인용된 총 횟수' in df.columns and '논문명' in df.columns:
        print("\n가장 많이 인용된 실존주의 관련 논문 Top 5:")
        # 횟수를 숫자로 다루기 위해 변환
        df['인용된 총 횟수'] = pd.to_numeric(df['인용된 총 횟수'], errors='coerce').fillna(0)
        top_cited = df.sort_values(by='인용된 총 횟수', ascending=False).head(5)
        
        for _, row in top_cited.iterrows():
            print(f"   -> [{int(row['인용된 총 횟수'])}회 인용] {row['논문명']}")
    else:
        print("\n경고: '인용된 총 횟수' 컬럼을 찾을 수 없습니다.")
    
    # 저자 키워드 확인
    if '저자키워드' in df.columns:
        print("\n주요 논문 키워드 엿보기:")
        keywords = df['저자키워드'].dropna().head(5)
        for _, kw in keywords.items():
            print(f"   -> {kw}")
        
    else:
        print("\n경고: '저자키워드' 컬럼을 찾을 수 없습니다.")

    print("\n분석이 완료되었습니다. 이 키워드들을 연결하면 '네트워크 그래프' 대시보드가 완성됩니다!")
    print("====================================")
