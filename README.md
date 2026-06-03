# 가계부 대시보드

Streamlit 기반의 개인 가계부 웹 대시보드입니다.  
CSV·Excel 파일을 업로드하면 월별·카테고리별 지출을 인터랙티브 차트로 시각화합니다.

---

## 기술 스택

| 역할 | 라이브러리 |
|------|-----------|
| 데이터 처리 | pandas |
| 파일 입출력 | openpyxl |
| 데이터 저장 | TinyDB (JSON) |
| 대시보드 UI | Streamlit |
| 차트 | Plotly |

---

## 프로젝트 구조

```
household-budget/
├── data/
│   ├── raw/            # 원본 CSV/Excel 파일
│   ├── processed/      # 전처리 결과
│   └── budget.json     # TinyDB 저장소 (자동 생성)
├── src/
│   ├── loader.py       # 파일 로딩 & 컬럼 표준화 (삼성카드 자동 감지 포함)
│   ├── categorizer.py  # 카테고리 목록 관리
│   ├── analyzer.py     # 월별/카테고리별 집계
│   ├── storage.py      # TinyDB 입출력
│   └── charts.py       # Plotly 차트 생성
├── dashboard/
│   └── app.py          # Streamlit 메인 앱
├── tests/
│   └── test_analyzer.py
└── requirements.txt
```

---

## 설치 및 실행

```bash
# 1. 저장소 클론
git clone https://github.com/ununbum/household-budget.git
cd household-budget

# 2. 가상환경 생성 및 활성화
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 대시보드 실행
streamlit run dashboard/app.py
```

브라우저에서 `http://localhost:8501` 로 접속합니다.

---

## 사용 방법

### 1. 데이터 업로드

좌측 사이드바에서 **CSV 또는 Excel(.xlsx)** 파일을 업로드합니다.

**지원 파일 형식**

| 형식 | 조건 |
|------|------|
| CSV | 인코딩 UTF-8 또는 UTF-8 BOM |
| Excel (.xlsx) | 일반 형식 또는 삼성카드 청구서 |

**일반 CSV/Excel 컬럼명 규칙** (자동 인식)

| 표준 컬럼 | 인식 가능한 이름 |
|-----------|----------------|
| 날짜 | `날짜` `date` `일자` |
| 금액 | `금액` `amount` `지출` `비용` |
| 항목 | `항목` `내용` `description` `내역` |
| 카테고리 | `카테고리` `category` `분류` |

**삼성카드 청구서** — 파일 내 시트명(`일시불`, `연회비-기타수수료`)을 자동 감지하여 별도 형식으로 파싱합니다. 컬럼 매핑 불필요.

### 2. 카테고리 지정

파일 업로드 후 표(data editor)가 표시됩니다.  
`카테고리` 열 셀을 클릭해 드롭다운에서 분류를 선택하고 **저장** 버튼을 누릅니다.

**기본 카테고리**

`식비` / `교통` / `주거/공과금` / `의료/건강` / `문화/여가` / `쇼핑` / `교육` / `기타`

### 3. 대시보드 조회

상단 **조회 월** 셀렉트박스로 전체 또는 특정 월을 필터링합니다.

| 차트 | 설명 |
|------|------|
| 월별 총 지출 (막대) | 월별 지출 합계 비교 |
| 카테고리별 지출 (도넛) | 선택 월의 항목 비중 |
| 월별 지출 추이 (라인) | 지출 흐름 파악 |
| 월×카테고리 히트맵 | 월별 카테고리 분포 한눈에 확인 |

하단 **전체 데이터 보기** 를 펼치면 원본 행 데이터를 테이블로 확인할 수 있습니다.

### 4. 데이터 초기화

사이드바 하단 **전체 데이터 초기화** 버튼으로 저장된 모든 내역을 삭제합니다.

---

## 테스트 실행

```bash
python -m pytest tests/ -v
```

---

## 데이터 저장 방식

모든 지출 내역은 `data/budget.json` (TinyDB) 에 누적 저장됩니다.  
앱을 재시작해도 데이터가 유지됩니다.  
민감 데이터 보호를 위해 `data/` 디렉토리는 `.gitignore` 에 포함되어 있습니다.
