"""헤드헌터 AI 에이전트 Streamlit 메인 앱"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.agents.workflow import get_headhunter_workflow
from src.agents.simple_agent import get_simple_headhunter_agent
from src.database.repositories import get_candidate_repository
from src.vector_store.faiss_store import get_vector_store
from src.utils.visualization import display_workflow_in_streamlit, display_beautiful_workflow_in_streamlit
from langchain_core.messages import HumanMessage, AIMessage

# 페이지 설정
st.set_page_config(
    page_title="헤드헌터 AI 에이전트",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    font-weight: bold;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}

.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}

.user-message {
    background-color: #e3f2fd;
    border-left: 4px solid #2196f3;
}

.bot-message {
    background-color: #f3e5f5;
    border-left: 4px solid #9c27b0;
}

.metric-card {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 0.5rem;
    border: 1px solid #dee2e6;
}
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'workflow' not in st.session_state:
    st.session_state.workflow = None

if 'simple_agent' not in st.session_state:
    st.session_state.simple_agent = None

if 'agent_mode' not in st.session_state:
    st.session_state.agent_mode = "simple"  # "simple" 또는 "advanced"

def initialize_simple_agent():
    """간단한 에이전트 초기화"""
    if st.session_state.simple_agent is None:
        try:
            st.session_state.simple_agent = get_simple_headhunter_agent()
            st.session_state.agent_mode = "simple"
            st.success("간단한 AI 에이전트가 초기화되었습니다!")
        except Exception as e:
            st.error(f"간단한 에이전트 초기화 중 오류 발생: {str(e)}")

def initialize_workflow():
    """고급 워크플로우 초기화"""
    if st.session_state.workflow is None:
        with st.spinner("고급 AI 에이전트를 초기화하는 중..."):
            try:
                workflow = get_headhunter_workflow()
                st.session_state.workflow = workflow.get_graph()
                st.session_state.agent_mode = "advanced"
                st.success("고급 AI 에이전트가 성공적으로 초기화되었습니다!")
            except Exception as e:
                st.error(f"고급 워크플로우 초기화 중 오류 발생: {str(e)}")
                st.info("간단한 에이전트로 전환합니다...")
                initialize_simple_agent()

def get_candidate_stats():
    """인재 통계 정보 조회"""
    try:
        repo = get_candidate_repository()
        stats = repo.get_statistics()
        return stats
    except Exception as e:
        st.error(f"통계 조회 중 오류: {str(e)}")
        return None

def get_knowledge_stats():
    """지식 베이스 통계 조회"""
    try:
        vector_store = get_vector_store()
        stats = vector_store.get_stats()
        return stats
    except Exception as e:
        st.error(f"지식 베이스 통계 조회 중 오류: {str(e)}")
        return None

def main():
    """메인 앱"""

    # 헤더
    st.markdown('<h1 class="main-header">🤖 헤드헌터 AI 에이전트</h1>', unsafe_allow_html=True)

    # 사이드바
    with st.sidebar:
        st.header("📊 대시보드")

        # 에이전트 모드 선택
        st.subheader("🤖 AI 에이전트")

        current_mode = "간단 모드" if st.session_state.agent_mode == "simple" else "고급 모드"
        st.write(f"**현재 모드**: {current_mode}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 간단 모드"):
                initialize_simple_agent()

        with col2:
            if st.button("⚡ 고급 모드"):
                initialize_workflow()

        st.markdown("---")

        # 인재 통계
        st.subheader("👥 인재 데이터베이스")
        candidate_stats = get_candidate_stats()
        if candidate_stats:
            st.metric("총 인재 수", candidate_stats['total_candidates'])

            # 지역별 분포
            if candidate_stats['location_distribution']:
                st.write("**지역별 분포**")
                for loc_info in candidate_stats['location_distribution'][:5]:
                    st.write(f"• {loc_info['location']}: {loc_info['count']}명")

            # 인기 스킬
            if candidate_stats['top_skills']:
                st.write("**인기 스킬 TOP 5**")
                for skill_info in candidate_stats['top_skills'][:5]:
                    st.write(f"• {skill_info['skill']}: {skill_info['count']}명")

        st.markdown("---")

        # 지식 베이스 통계
        st.subheader("📚 지식 베이스")
        knowledge_stats = get_knowledge_stats()
        if knowledge_stats:
            st.metric("총 문서 수", knowledge_stats['total_documents'])

            if knowledge_stats['categories']:
                st.write("**카테고리별 분포**")
                for category, count in knowledge_stats['categories'].items():
                    st.write(f"• {category}: {count}건")

    # 메인 영역 - 탭으로 구성
    tab1, tab2, tab3, tab4 = st.tabs(["💬 AI 상담", "👥 인재 검색", "📈 시장 분석", "🔄 워크플로우"])

    with tab1:
        st.header("💬 헤드헌터 AI 상담")

        # 채팅 인터페이스
        chat_container = st.container()

        # 이전 메시지들 표시
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f'<div class="chat-message user-message"><strong>👤 사용자:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-message bot-message"><strong>🤖 AI 에이전트:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)

        # 입력 영역
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("질문을 입력하세요:", placeholder="예: Python 개발자 5년 이상 경력자를 찾아줘")
            submitted = st.form_submit_button("전송")

            if submitted and user_input:
                # 사용자 메시지 추가
                st.session_state.messages.append({"role": "user", "content": user_input})

                # AI 응답 생성
                ai_response = None

                # 에이전트 모드에 따라 처리
                if st.session_state.agent_mode == "simple":
                    # 간단한 에이전트 사용
                    if st.session_state.simple_agent is None:
                        initialize_simple_agent()

                    if st.session_state.simple_agent:
                        with st.spinner("AI가 답변을 생성하는 중..."):
                            try:
                                ai_response = st.session_state.simple_agent.chat(
                                    user_input,
                                    st.session_state.messages[:-1]  # 방금 추가한 메시지 제외
                                )
                            except Exception as e:
                                ai_response = f"죄송합니다. 오류가 발생했습니다: {str(e)}"

                elif st.session_state.agent_mode == "advanced":
                    # 고급 워크플로우 사용
                    if st.session_state.workflow is None:
                        st.warning("고급 모드를 초기화하는 중...")
                        initialize_workflow()

                    if st.session_state.workflow:
                        with st.spinner("고급 AI가 답변을 생성하는 중..."):
                            try:
                                # 전체 대화 기록을 LangGraph 메시지로 변환
                                langraph_messages = []
                                for msg in st.session_state.messages:
                                    if msg["role"] == "user":
                                        langraph_messages.append(HumanMessage(content=msg["content"]))
                                    elif msg["role"] == "assistant":
                                        langraph_messages.append(AIMessage(content=msg["content"]))

                                # 워크플로우 실행
                                result = st.session_state.workflow.invoke(
                                    {"messages": langraph_messages},
                                    config={"configurable": {"thread_id": "main_thread"}}
                                )

                                # AI 응답 추출
                                if result and "messages" in result and len(result["messages"]) > 0:
                                    ai_response = result["messages"][-1].content
                                else:
                                    ai_response = "죄송합니다. 고급 모드에서 응답을 생성할 수 없습니다. 간단한 모드로 전환해주세요."

                            except Exception as e:
                                st.error(f"고급 모드 오류: {str(e)}")
                                ai_response = "고급 모드에서 오류가 발생했습니다. 간단한 모드로 전환을 권장합니다."

                # 기본 응답 처리
                if not ai_response:
                    ai_response = "에이전트가 초기화되지 않았습니다. 사이드바에서 AI 에이전트를 초기화해주세요."

                # AI 응답 추가
                if ai_response:
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})

                # 페이지 새로고침
                st.rerun()

        # 예시 질문들
        st.markdown("---")
        st.subheader("💡 예시 질문들")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**정형 데이터 검색 (PostgreSQL)**")
            example_questions_1 = [
                "Python 개발자 5년 이상 경력자를 찾아줘",
                "강남구에 거주하는 React 개발자 리스트를 보여줘",
                "연봉 8천만원 이상 희망하는 백엔드 개발자가 몇 명이야?",
                "원격근무를 선호하는 AI 엔지니어를 찾아줘"
            ]

            for question in example_questions_1:
                if st.button(question, key=f"q1_{hash(question)}"):
                    st.session_state.messages.append({"role": "user", "content": question})
                    st.rerun()

        with col2:
            st.markdown("**비정형 데이터 검색 (Vector DB + Web)**")
            example_questions_2 = [
                "최근 AI 개발자 시장 트렌드가 어때?",
                "클라우드 엔지니어의 평균 연봉은 얼마나 돼?",
                "2024년 개발자 채용 시장 최신 동향을 웹에서 찾아줘",
                "스타트업에서 요구하는 핵심 기술스택이 뭐야?"
            ]

            for question in example_questions_2:
                if st.button(question, key=f"q2_{hash(question)}"):
                    st.session_state.messages.append({"role": "user", "content": question})
                    st.rerun()

    with tab2:
        st.header("👥 인재 검색 필터")

        # 검색 필터 UI
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("기본 조건")
            skills = st.multiselect("기술 스킬", ["Python", "JavaScript", "React", "Node.js", "AWS", "Docker", "Kubernetes"])
            location = st.selectbox("지역", ["전체", "서울특별시", "경기도", "부산광역시", "대구광역시"])
            work_type = st.selectbox("근무 형태", ["전체", "remote", "hybrid", "onsite"])

        with col2:
            st.subheader("경력 & 급여")
            min_exp = st.slider("최소 경력 (년)", 0, 15, 0)
            salary_range = st.slider("희망 연봉 (만원)", 3000, 15000, (5000, 10000))
            availability = st.selectbox("구직 상태", ["전체", "actively_looking", "passively_looking", "not_looking"])

        with col3:
            st.subheader("산업 분야")
            industry = st.selectbox("희망 산업", ["전체", "Technology", "Fintech", "E-commerce", "AI/ML", "Gaming"])
            age_range = st.slider("나이", 20, 50, (25, 40))

        if st.button("🔍 검색 실행"):
            # 검색 파라미터 구성
            search_query = f"다음 조건으로 인재를 찾아줘: "
            conditions = []

            if skills:
                conditions.append(f"기술스킬: {', '.join(skills)}")
            if location != "전체":
                conditions.append(f"지역: {location}")
            if work_type != "전체":
                conditions.append(f"근무형태: {work_type}")
            if min_exp > 0:
                conditions.append(f"최소경력: {min_exp}년")
            if salary_range != (5000, 10000):
                conditions.append(f"연봉: {salary_range[0]}-{salary_range[1]}만원")
            if availability != "전체":
                conditions.append(f"구직상태: {availability}")
            if industry != "전체":
                conditions.append(f"산업: {industry}")

            search_query += ", ".join(conditions)

            # 메시지에 추가하고 AI 상담 탭으로 이동
            st.session_state.messages.append({"role": "user", "content": search_query})
            st.success("검색 조건이 AI 상담으로 전송되었습니다. 'AI 상담' 탭에서 결과를 확인하세요.")

    with tab3:
        st.header("📈 시장 분석")

        # 시장 분석 퀵 버튼들
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🔍 시장 트렌드")

            if st.button("📊 2024 개발자 시장 동향"):
                query = "2024년 한국 개발자 시장 동향과 트렌드를 분석해줘"
                st.session_state.messages.append({"role": "user", "content": query})
                st.success("분석 요청이 전송되었습니다.")

            if st.button("💰 직무별 연봉 분석"):
                query = "개발자 직무별 연봉 현황과 트렌드를 알려줘"
                st.session_state.messages.append({"role": "user", "content": query})
                st.success("분석 요청이 전송되었습니다.")

            if st.button("🏠 원격근무 트렌드"):
                query = "개발자 원격근무 트렌드와 선호도를 분석해줘"
                st.session_state.messages.append({"role": "user", "content": query})
                st.success("분석 요청이 전송되었습니다.")

        with col2:
            st.subheader("🏢 산업별 분석")

            if st.button("🤖 AI/ML 산업 전망"):
                query = "AI/ML 개발자 시장 전망과 요구사항을 분석해줘"
                st.session_state.messages.append({"role": "user", "content": query})
                st.success("분석 요청이 전송되었습니다.")

            if st.button("💳 핀테크 시장 동향"):
                query = "핀테크 산업의 개발자 채용 동향을 알려줘"
                st.session_state.messages.append({"role": "user", "content": query})
                st.success("분석 요청이 전송되었습니다.")

            if st.button("🛒 이커머스 기술 트렌드"):
                query = "이커머스 분야의 기술 트렌드와 인재 수요를 분석해줘"
                st.session_state.messages.append({"role": "user", "content": query})
                st.success("분석 요청이 전송되었습니다.")

    with tab4:
        st.header("🔄 AI 에이전트 워크플로우")

        # 워크플로우 시각화 표시
        try:
            # Customer Support Agent 스타일의 아름다운 워크플로우 시각화
            display_beautiful_workflow_in_streamlit()
        except Exception as e:
            st.error(f"Beautiful 워크플로우 시각화 로드 중 오류 발생: {e}")
            st.info("대체 워크플로우 시각화를 시도합니다...")

            # 대체: 기존 워크플로우 시각화
            try:
                display_workflow_in_streamlit()
            except Exception as e2:
                st.error(f"워크플로우 시각화 로드 중 오류 발생: {e2}")
                st.info("워크플로우 시각화를 위해서는 matplotlib과 plotly가 필요합니다.")

    # 하단 정보
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        🤖 헤드헌터 AI 에이전트 | PostgreSQL + FAISS Vector DB + Solar LLM + Tavily Web Search
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()