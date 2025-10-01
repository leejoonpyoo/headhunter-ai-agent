# 🤖 헤드헌터 AI 에이전트

HR을 도와주는 지능형 헤드헌터 에이전트입니다. 정형 데이터베이스와 벡터 검색을 결합하여 인재 매칭, 시장 분석, 실시간 정보 검색을 제공합니다.

## 🏗️ 아키텍처

```mermaid
graph TB
    A[사용자 질문] --> B[LangGraph 워크플로우]
    B --> C[Query 분류기]

    C --> D[인재 검색 에이전트]
    C --> E[시장 분석 에이전트]
    C --> F[웹 검색 에이전트]
    C --> G[통합 상담 에이전트]

    D --> H[PostgreSQL<br/>정형 데이터]
    E --> I[FAISS Vector DB<br/>비정형 데이터]
    F --> J[Tavily Web Search<br/>실시간 정보]

    H --> K[결과 통합]
    I --> K
    J --> K

    K --> L[Streamlit UI]
```

### 📊 데이터 분리 전략

- **정형 데이터 (PostgreSQL)**: 인재의 구조화된 정보
  - 개인정보, 경력, 스킬, 학력, 희망조건
  - SQL 쿼리로 정확한 필터링

- **비정형 데이터 (FAISS Vector DB)**: 시장 정보와 지식
  - 기술 트렌드, 시장 분석, 산업 전망, 급여 정보
  - 의미적 벡터 검색

- **실시간 데이터 (Tavily Web Search)**: 최신 정보
  - 채용공고, 회사 정보, 뉴스, 시장 동향

## 🛠️ 기술 스택

- **LangGraph**: AI 에이전트 워크플로우 오케스트레이션
- **Solar LLM (Upstage)**: 대화형 AI 모델
- **PostgreSQL**: 정형 데이터 저장소
- **FAISS**: 벡터 검색 엔진
- **Sentence Transformers**: 무료 임베딩 모델 (`jhgan/ko-sroberta-multitask`)
- **Tavily**: 실시간 웹 검색
- **Streamlit**: 웹 인터페이스
- **Docker**: 데이터베이스 컨테이너화

## 🚀 설치 및 실행

### 1. 프로젝트 클론
```bash
git clone <repository-url>
cd headhunter-ai-agent
```

### 2. 가상환경 설정
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. PostgreSQL 실행
```bash
docker-compose up -d
```

### 5. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일에서 API 키들을 실제 값으로 변경
```

필수 환경 변수:
```env
UPSTAGE_API_KEY=your_upstage_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
DB_URL=postgresql://headhunter_user:headhunter_pass@localhost:5432/headhunter_db
```

### 6. 프로젝트 초기화
```bash
python setup_project.py
```

### 7. Streamlit 앱 실행
```bash
python streamlit_run.py
```

또는

```bash
streamlit run src/streamlit_app/main.py
```

브라우저에서 `http://localhost:8501` 접속

## 📖 사용법

### Streamlit 웹 인터페이스

1. **AI 상담 탭**: 자연어로 질문하고 AI 에이전트와 대화
2. **인재 검색 탭**: 필터를 사용하여 구체적인 조건으로 인재 검색
3. **시장 분석 탭**: 시장 트렌드와 산업 분석 정보 조회

### Tool 추가 가이드

새로운 기능을 추가하려면:

1. `src/tools/` 디렉토리에 새 파일 생성
2. `@tool` 데코레이터로 함수 정의
3. Type hints와 docstring 필수 작성
4. `src/agents/workflow.py`에서 새 툴을 에이전트에 바인딩

예시:
```python
from langchain_core.tools import tool

@tool
def new_search_function(query: str, limit: int = 5) -> Dict[str, Any]:
    """새로운 검색 기능

    Args:
        query: 검색 쿼리
        limit: 최대 결과 수

    Returns:
        검색 결과
    """
    # 구현 코드
    return {"results": []}
```

## 🧪 테스트용 예상 질문들

### 정형 데이터 RAG 테스트 (PostgreSQL)

```
✅ 기본 스킬 검색
"Python 개발자 5년 이상 경력자를 찾아줘"

✅ 지역 + 기술 조합
"강남구에 거주하는 React 개발자 리스트를 보여줘"

✅ 급여 조건 검색
"연봉 8천만원 이상 희망하는 백엔드 개발자가 몇 명이야?"

✅ 근무 형태 검색
"원격근무를 선호하는 AI 엔지니어를 찾아줘"

✅ 복합 조건 검색
"서울에 거주하고 AWS 경험 3년 이상인 DevOps 엔지니어 중 적극적으로 구직중인 사람 찾아줘"

✅ 구직 상태별 검색
"현재 적극적으로 구직활동 중인 프론트엔드 개발자는 몇 명이야?"

✅ 산업별 선호도
"핀테크 산업을 희망하는 개발자들 리스트를 보여줘"

✅ 특정 인재 상세 조회
"ID 3번 인재의 상세 정보를 알려줘"
```

### 비정형 데이터 RAG 테스트 (FAISS Vector DB)

```
✅ 기술 정보 검색
"Python 기술의 특징과 사용 분야에 대해 알려줘"

✅ 시장 트렌드 분석
"최근 AI 개발자 시장 트렌드가 어때?"

✅ 급여 정보 검색
"데이터 사이언티스트의 평균 연봉은 얼마나 돼?"

✅ 산업 분석
"핀테크 산업의 개발자 수요와 전망은 어떤가?"

✅ 기술 비교
"React와 Vue.js를 비교해줘"

✅ 근무 형태 트렌드
"개발자들의 원격근무 선호도 트렌드를 알려줘"

✅ 기술별 시장 상황
"클라우드 엔지니어 시장은 어떤 상황이야?"
```

### Tool Calling 복합 기능 테스트

```
✅ 정형 + 비정형 조합
"서울 지역 풀스택 개발자 중에서 원격근무 선호하는 사람들의 시장 동향도 같이 알려줘"

✅ 인재 검색 + 시장 분석
"데이터 사이언티스트 후보자들과 현재 데이터 사이언스 분야 전망을 함께 분석해줘"

✅ 다단계 분석
"Python 개발자 현황을 보여주고, Python 기술 트렌드와 시장 전망도 함께 분석해줘"

✅ 조건부 추천
"5년차 백엔드 개발자가 다음 커리어로 고려할 만한 기술스택과 해당 분야 인재들은?"
```

### 외부 데이터 검색 테스트 (Tavily Web Search)

```
✅ 최신 시장 동향
"2024년 개발자 채용 시장 최신 동향을 웹에서 찾아줘"

✅ 특정 회사 채용 정보
"네이버에서 현재 채용중인 개발자 포지션이 뭐가 있어?"

✅ 기술 뉴스
"최근 ChatGPT와 관련된 개발자 시장 뉴스를 찾아줘"

✅ 급여 벤치마크
"2024년 시니어 개발자 연봉 현황을 최신 정보로 알려줘"

✅ 스타트업 투자 동향
"최근 스타트업 투자 및 개발자 채용 뉴스를 찾아줘"

✅ 회사별 정보
"토스에서 개발자 채용 정보와 회사 문화를 조사해줘"
```

### 통합 상담 테스트

```
✅ 커리어 컨설팅
"3년차 프론트엔드 개발자인데, 다음 단계로 뭘 준비해야 할까? 시장 상황과 함께 알려줘"

✅ 이직 준비 가이드
"현재 Java 백엔드 개발자인데 AI 분야로 전환하고 싶어. 관련 인재들과 시장 상황을 분석해줘"

✅ 급여 협상 자료
"5년차 풀스택 개발자의 적정 연봉과 시장 데이터를 종합적으로 분석해줘"

✅ 채용 전략 수립
"스타트업에서 시니어 Python 개발자를 채용하려면 어떤 조건과 전략이 필요할까?"
```

## 📁 프로젝트 구조

```
headhunter-ai-agent/
├── src/
│   ├── database/           # PostgreSQL 관련
│   │   ├── connection.py   # DB 연결 관리
│   │   ├── models.py       # SQLAlchemy 모델
│   │   └── repositories.py # 데이터 액세스 레이어
│   │
│   ├── vector_store/       # FAISS 벡터 스토어
│   │   ├── embedder.py     # 무료 임베딩 모델
│   │   ├── faiss_store.py  # 벡터 검색
│   │   └── knowledge_loader.py # 지식 데이터 로딩
│   │
│   ├── tools/              # LangChain 도구들
│   │   ├── candidate_tools.py    # 인재 검색 (정형)
│   │   ├── market_tools.py       # 시장 정보 (비정형)
│   │   └── web_search_tools.py   # 웹 검색 (실시간)
│   │
│   ├── agents/             # LangGraph 에이전트
│   │   └── workflow.py     # 워크플로우 오케스트레이션
│   │
│   └── streamlit_app/      # 웹 인터페이스
│       └── main.py         # Streamlit 메인 앱
│
├── database/               # DB 스키마 및 샘플 데이터
├── data/                   # 벡터 DB용 지식 데이터
├── docker-compose.yml      # PostgreSQL 컨테이너
├── requirements.txt        # Python 의존성
└── setup_project.py        # 프로젝트 초기화 스크립트
```

## 🔧 개발 환경

- Python 3.8+
- PostgreSQL 15+
- Docker & Docker Compose
- Git

## 📝 API 키 발급

### 1. Upstage API (Solar LLM)
- [Upstage Console](https://console.upstage.ai/) 회원가입
- API 키 발급

### 2. Tavily API (웹 검색)
- [Tavily](https://tavily.com/) 회원가입
- 무료 API 키 발급

## 🐛 트러블슈팅

### PostgreSQL 연결 오류
```bash
# Docker 컨테이너 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs postgres

# 재시작
docker-compose restart postgres
```

### 임베딩 모델 다운로드 오류
```bash
# 수동으로 모델 다운로드
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('jhgan/ko-sroberta-multitask')"
```

### Streamlit 실행 오류
```bash
# 환경 변수 확인
python -c "import os; print(os.getenv('UPSTAGE_API_KEY'))"

# 패키지 재설치
pip install --upgrade -r requirements.txt
```

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🙏 감사의 말

- [LangChain](https://langchain.com/) - AI 애플리케이션 프레임워크
- [Upstage](https://upstage.ai/) - Solar LLM 제공
- [Tavily](https://tavily.com/) - 웹 검색 API
- [Sentence Transformers](https://www.sbert.net/) - 무료 임베딩 모델