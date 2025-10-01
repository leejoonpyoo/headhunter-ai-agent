# 📁 프로젝트 구조

## 최적화된 프로젝트 구조

```
headhunter-ai-agent/
├── 📄 run.py                    # ⭐ 메인 실행 파일 (챗봇 시작)
├── 📄 run.bat                   # Windows용 실행 파일
│
├── 📂 src/                      # 소스 코드
│   ├── 📂 agents/              # AI 에이전트
│   │   └── react_agent.py      # ⭐ ReAct 에이전트 (메인)
│   │
│   ├── 📂 tools/               # AI 도구들
│   │   ├── candidate_tools.py  # 인재 검색 (PostgreSQL)
│   │   ├── market_tools.py     # 시장 분석 (RAG)
│   │   └── web_search_tools.py # 웹 검색 (Tavily)
│   │
│   ├── 📂 database/            # 데이터베이스
│   │   ├── connection.py
│   │   ├── models.py
│   │   └── repositories.py
│   │
│   ├── 📂 vector_store/        # RAG 벡터 스토어
│   │   ├── embedder.py
│   │   ├── faiss_store.py
│   │   └── knowledge_loader.py
│   │
│   └── 📂 streamlit_app/       # UI
│       ├── chatbot_app.py      # ⭐ 메인 챗봇 UI
│       └── main.py             # 기본 검색 UI
│
├── 📂 data/                     # 데이터
│   ├── structured/             # 정형 데이터 (CSV)
│   │   ├── company_info.csv
│   │   ├── talent_profile.csv
│   │   ├── exp_tag.csv
│   │   └── company_external_data.csv
│   │
│   └── unstructured/           # 비정형 데이터 (RAG)
│       ├── knowledge/          # 지식 베이스
│       │   ├── tech_info.txt
│       │   ├── market_trends.txt
│       │   └── salary_info.txt
│       └── vector_store/       # FAISS 인덱스 (자동 생성)
│
├── 📂 scripts/                  # 유틸리티 스크립트
│   ├── import_data.py          # 데이터 임포트
│   ├── install_deps.bat        # 의존성 설치
│   └── run_chatbot.py          # 레거시 실행 스크립트
│
├── 📂 _backup/                  # 백업 (git ignored)
│   ├── old_code/               # 사용하지 않는 코드
│   ├── deprecated/             # 폐기된 폴더
│   └── tests/                  # 테스트 파일
│
├── 📄 README.md                 # 메인 문서
├── 📄 QUICKSTART.md             # 빠른 시작 가이드
├── 📄 PROJECT_STRUCTURE.md      # 이 파일
├── 📄 requirements.txt          # Python 의존성
├── 📄 docker-compose.yml        # PostgreSQL 설정
├── 📄 .env.example             # 환경 변수 템플릿
└── 📄 .gitignore               # Git 제외 파일
```

## 주요 파일 설명

### 실행 파일
- **[run.py](run.py)** - 챗봇 실행 (권장)
- **[run.bat](run.bat)** - Windows 더블클릭 실행

### 핵심 코드
- **[src/agents/react_agent.py](src/agents/react_agent.py)** - ReAct 에이전트 (추론+행동)
- **[src/streamlit_app/chatbot_app.py](src/streamlit_app/chatbot_app.py)** - 메인 UI
- **[src/tools/](src/tools/)** - 20+ AI 도구

### 데이터
- **[data/structured/](data/structured/)** - CSV 정형 데이터
- **[data/unstructured/](data/unstructured/)** - RAG 지식 베이스

### 설정
- **[.env](.env.example)** - API 키 설정
- **[requirements.txt](requirements.txt)** - 패키지 목록
- **[docker-compose.yml](docker-compose.yml)** - DB 설정

## 삭제된 파일/폴더 (백업으로 이동)

### `_backup/old_code/`
- `workflow.py`, `simple_agent.py`, `enhanced_workflow.py` - 구버전 에이전트
- `streamlit_run.py`, `setup_project.py` - 사용하지 않는 스크립트
- `talent_tools.py`, `visualization_tools.py` - 중복 도구
- `src/utils/` - 사용하지 않는 유틸리티

### `_backup/deprecated/`
- `meta-llama-academy-RagLLama/` - 중복 폴더
- `notebooks/`, `notebooks-sample/` - 노트북 (미사용)
- `database/`, `vector_store/` - 루트 레벨 중복 폴더

### `_backup/tests/`
- `tests/` - 테스트 파일들

## 간소화된 워크플로우

### 개발 시작
```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. PostgreSQL 시작
docker-compose up -d

# 3. 데이터 임포트
python scripts/import_data.py

# 4. 챗봇 실행
python run.py
```

### 파일 구조 원칙
✅ **유지**: 실제 사용 중인 파일만
✅ **정리**: 명확한 폴더 구조
✅ **백업**: 삭제 대신 `_backup/`으로 이동
✅ **문서화**: 모든 주요 파일 설명

## 각 폴더 역할

| 폴더 | 역할 | 파일 수 |
|------|------|---------|
| `src/agents/` | AI 에이전트 | 1 (react_agent.py) |
| `src/tools/` | AI 도구 | 3 (candidate, market, web) |
| `src/database/` | DB 연결/모델 | 3 |
| `src/vector_store/` | RAG 시스템 | 3 |
| `src/streamlit_app/` | UI | 2 (chatbot, main) |
| `data/structured/` | 정형 데이터 | 4 CSV |
| `data/unstructured/` | RAG 데이터 | 3 TXT + 벡터 DB |
| `scripts/` | 유틸리티 | 3 |
| `_backup/` | 백업 | 다수 (git ignored) |

## Git 관리

**추적 대상**:
- 소스 코드 (`src/`)
- 문서 (`*.md`)
- 설정 파일 (`requirements.txt`, `docker-compose.yml`)
- 실행 파일 (`run.py`, `run.bat`)

**무시 대상** (`.gitignore`):
- `_backup/` - 백업 파일
- `venv/` - 가상환경
- `.env` - 환경 변수
- `__pycache__/` - Python 캐시
- `data/unstructured/vector_store/` - FAISS 인덱스 (자동 생성)

## 다음 단계

프로젝트 구조가 최적화되었습니다! 이제:

1. ✅ 코드 정리 완료
2. ✅ 실행 파일 통합
3. ✅ 백업 시스템 구축
4. ✅ 문서화 완료

**사용법**:
```bash
python run.py
```

또는:
```bash
run.bat
```

That's it! 🎉
