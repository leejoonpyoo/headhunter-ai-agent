# 🚀 빠른 시작 가이드

## 1. 필수 패키지 설치

터미널을 열고 다음 명령어를 실행하세요:

```bash
# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 모든 필수 패키지 설치
pip install -r requirements.txt
```

또는 개별 설치:

```bash
pip install streamlit langchain langchain-core langchain-upstage langgraph
pip install sentence-transformers faiss-cpu psycopg2-binary python-dotenv tavily-python
```

## 2. 환경 변수 설정

`.env` 파일을 생성하고 API 키를 입력하세요:

```env
UPSTAGE_API_KEY=your_upstage_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
DB_URL=postgresql://headhunter_user:headhunter_pass@localhost:5432/headhunter_db
```

### API 키 발급 방법

**Upstage API:**
1. https://console.upstage.ai/ 방문
2. 회원가입 및 로그인
3. API 키 생성
4. `.env` 파일에 복사

**Tavily API:**
1. https://tavily.com/ 방문
2. 회원가입
3. 무료 API 키 발급
4. `.env` 파일에 복사

## 3. 데이터베이스 시작

```bash
docker-compose up -d
```

## 4. 데이터 임포트

```bash
python import_data.py
```

## 5. 챗봇 실행!

### 방법 1: Python 스크립트 (권장)
```bash
python run_chatbot.py
```

### 방법 2: 직접 Streamlit 실행
```bash
streamlit run src/streamlit_app/chatbot_app.py
```

### 방법 3: Windows 배치 파일
```bash
run_chatbot.bat
```

## 6. 브라우저 접속

브라우저가 자동으로 열리거나, 수동으로 다음 주소로 접속:

```
http://localhost:8501
```

## ✅ 정상 작동 확인

챗봇이 실행되면 다음과 같은 테스트 질문을 해보세요:

```
"안녕하세요!"
"Python 개발자를 찾고 있어요"
"데이터 사이언티스트 평균 연봉이 궁금해요"
```

## ⚠️ 문제 해결

### 1. ModuleNotFoundError
```bash
pip install --upgrade -r requirements.txt
```

### 2. Database Connection Error
```bash
docker-compose restart postgres
docker-compose ps
```

### 3. API Key Error
- `.env` 파일이 프로젝트 루트에 있는지 확인
- API 키가 올바른지 확인

### 4. Encoding Error (Windows)
- `run_chatbot.py`가 최신 버전인지 확인
- UTF-8 인코딩 문제는 자동으로 처리됩니다

### 5. Port Already in Use
```bash
# 다른 포트로 실행
streamlit run src/streamlit_app/chatbot_app.py --server.port 8502
```

## 📚 더 알아보기

- 전체 문서: [README.md](README.md)
- 프로젝트 구조: [README.md#프로젝트-구조](README.md#-프로젝트-구조)
- 테스트 쿼리: [README.md#테스트-쿼리-예시](README.md#-테스트-쿼리-예시)

## 🎯 다음 단계

1. ✅ 챗봇과 대화하기
2. ✅ 복합 검색 쿼리 테스트
3. ✅ 사용자 정의 도구 추가
4. ✅ RAG 지식 베이스 확장

## 💬 도움이 필요하신가요?

GitHub Issues에 문의하거나 README의 Troubleshooting 섹션을 확인하세요!

---

Happy Headhunting! 🎉
