"""Streamlit 앱 실행 스크립트"""

import streamlit as st
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# 환경 변수 확인
from dotenv import load_dotenv
load_dotenv()

required_env_vars = [
    'UPSTAGE_API_KEY',
    'TAVILY_API_KEY',
    'DB_URL'
]

missing_vars = [var for var in required_env_vars if not os.getenv(var)]

if missing_vars:
    st.error(f"다음 환경 변수가 설정되지 않았습니다: {', '.join(missing_vars)}")
    st.error("먼저 .env 파일을 설정해주세요.")
    st.stop()

# 메인 앱 실행
if __name__ == "__main__":
    # Streamlit 설정
    os.system("streamlit run src/streamlit_app/main.py --server.port 8501 --server.address localhost")