# 🌌 ANTIGRAVITY NAV: 실존주의 '자유' 연구 동향 모니터링 대시보드

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Data Source](https://img.shields.io/badge/Data-KCI_(한국학술지인용색인)-blue)
![Stack](https://img.shields.io/badge/Tech-Python_|_HTML_|_ECharts-orange)

사르트르를 위시한 **실존주의 철학** 내에서 **'자유(Freedom)'**라는 개념이 학술적으로 어떻게 다루어지고 있는지 시각적으로 추적하기 위한 데이터 기반 웹 대시보드 프로젝트입니다. 차량의 대시보드처럼 직관적이고 세련된 다크 테마(Premium Dark UI)를 탑재했습니다.

## 📸 대시보드 미리보기

![대시보드 완성 화면](C:/Users/User/.gemini/antigravity/brain/1151844b-3328-4cfa-ad9b-7713aaf77434/dashboard_full_view_1776233697818.png)

## ✨ 핵심 기능 (Dashboard Features)

1. **📊 영향력 랭킹 (Focus Gauge):** KCI 피인용 횟수 기준 Top 10 핵심 문헌을 추출하여 철학 연구의 기준점 도출.
2. **🕸️ 개념 인지망 (Navigation Map):** '자유'를 중심으로 공저자 키워드(Author Keywords) 네트워크를 거미줄 형태로 시각화하여 밀접한 학술적 관계망 확인. (Force-directed graph 적용)
3. **📈 연구 밀도 변화 (Timeline):** 연도별 관련 논문 발행 빈도 변화를 부드러운 타임라인 영역 차트로 제공하여 시대적 관심도 추이 파악.

---

## 📂 프로젝트 구조

```text
📦 진성이의 실존주의/
 ├── 📄 GEMINI.md           # 본 프로젝트의 초기 기획서 및 구조 설계도
 ├── 📂 downloads/          # [원본] KCI 원본 논문 데이터 (보안상 제외됨)
 ├── 📂 scripts/            # [파이프라인] 데이터 가공을 위한 파이썬 스크립트
 │    └── process_data.py   
 ├── 📂 output/             # [결과물] 스크립트 전처리 후 생성된 JSON 파일
 │    └── dashboard_data.json
 └── 📂 web/                # [시각화] 웹 대시보드 화면 코드 환경
      ├── index.html        # 메인 대시보드 HTML
      ├── style.css         # 글래스모피즘 & 프리미엄 다크 테마 CSS 
      └── app.js            # ECharts를 이용한 자바스크립트 그래프 렌더링
```

---

## 🚀 실행 가이드 (How to Run)

### 1. 환경 분석 세팅 (Python)
KCI 데이터를 불러와서 웹 화면용 데이터(JSON)로 전처리하기 위해 패키지 설치가 필요합니다.
```bash
# 필수 라이브러리 설치
pip install pandas openpyxl lxml html5lib

# 데이터 전처리 파이프라인 가동
python scripts/process_data.py
```
> *※ 명령어가 성공적으로 실행되면 `output/dashboard_data.json` 정제 파일이 자동 생성됩니다.*

### 2. 웹 대시보드 실행 (Local Server)
HTML 파일을 단순 클릭하면 로컬 브라우저 보안 에러(CORS 오류)로 인해 그래프 데이터가 불러와지지 않을 수 있습니다. 파이썬 기본 제공 라이브러리를 통해 로컬 서버를 실행하세요.

```bash
# 프로젝트 가장 바깥쪽 폴더에서 서버 실행
python -m http.server 8000
```
- 인터넷 주소창에 `http://localhost:8000/web/index.html` 을 입력하여 확인하세요!

---

## 📝 엮은이 노트
* **개발 AI 도구**: Google Gemini (Antigravity Assistant)
* **초기 기획 모드 및 구현 승인 로직 적용 완료.**
