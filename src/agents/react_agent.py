"""ReAct 스타일 헤드헌터 AI 에이전트 - 완전한 구현"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_upstage import ChatUpstage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# 도구들 임포트
from ..tools.candidate_tools import (
    search_candidates_by_skills,
    search_candidates_by_location,
    search_candidates_by_salary_range,
    search_candidates_by_work_type,
    search_candidates_by_industry,
    search_candidates_by_availability,
    get_candidate_details,
    complex_candidate_search,
    get_candidate_statistics,
    search_companies_by_name,
    search_companies_by_category
)

from ..tools.market_tools import (
    search_tech_information,
    search_market_trends,
    search_industry_analysis,
    search_salary_information,
    general_knowledge_search,
    compare_technologies,
    get_knowledge_base_stats
)

from ..tools.web_search_tools import (
    web_search_latest_trends,
    search_job_postings,
    search_company_information,
    search_salary_benchmarks,
    search_tech_news,
    search_startup_funding_news
)

load_dotenv()

# 시스템 프롬프트
HEADHUNTER_SYSTEM_PROMPT = """당신은 전문 헤드헌터 AI 어시스턴트입니다.

## 역할
- 인재 검색 및 매칭
- 시장 동향 분석
- 기술 트렌드 연구
- 채용 시장 정보 제공
- 커리어 상담

## 사용 가능한 데이터 소스
1. **정형 데이터 (PostgreSQL)**: 인재 프로필, 회사 정보, 경험 태그
2. **비정형 데이터 (FAISS RAG)**: 기술 정보, 시장 트렌드, 급여 정보
3. **실시간 데이터 (Tavily 웹 검색)**: 최신 채용 공고, 뉴스, 회사 정보

## 도구 사용 가이드

### 인재 검색 도구 (PostgreSQL)
- `search_candidates_by_skills`: 기술 스킬로 검색
- `search_candidates_by_location`: 지역으로 검색
- `search_candidates_by_salary_range`: 급여 범위로 검색
- `search_candidates_by_work_type`: 근무 형태로 검색
- `search_candidates_by_industry`: 산업 분야로 검색
- `complex_candidate_search`: 여러 조건 복합 검색
- `get_candidate_details`: 특정 후보자 상세 정보

### 시장 분석 도구 (FAISS RAG)
- `search_tech_information`: 기술 관련 정보 검색
- `search_market_trends`: 시장 트렌드 분석
- `search_industry_analysis`: 산업 분석
- `search_salary_information`: 급여 정보
- `compare_technologies`: 기술 비교

### 웹 검색 도구 (Tavily)
- `web_search_latest_trends`: 최신 트렌드 검색
- `search_job_postings`: 채용 공고 검색
- `search_company_information`: 회사 정보 검색
- `search_tech_news`: 기술 뉴스

## 응답 가이드라인
1. **친절하고 전문적인 톤**: 존댓말 사용, 명확한 설명
2. **구체적인 데이터 제공**: 도구를 활용해 정확한 정보 제공
3. **실행 가능한 조언**: 단순 정보 나열이 아닌 실질적 가이드
4. **복합적 분석**: 여러 도구를 조합하여 종합적 분석
5. **추가 질문 유도**: 더 나은 서비스를 위한 추가 정보 요청

## 예시 대화 패턴

사용자: "Python 개발자를 찾고 있어요"
어시스턴트:
1. search_candidates_by_skills로 Python 개발자 검색
2. search_tech_information으로 Python 시장 동향 조회
3. 결과 종합하여 후보자 리스트와 시장 분석 제공
4. "어떤 경력 수준을 원하시나요?" 등 추가 질문

사용자: "데이터 사이언티스트 연봉이 궁금해요"
어시스턴트:
1. search_salary_information으로 내부 데이터 조회
2. web_search_latest_trends로 최신 시장 급여 정보 검색
3. 두 결과를 종합하여 평균 급여, 범위, 트렌드 분석

항상 사용자의 의도를 정확히 파악하고, 적절한 도구를 선택하여 최고의 답변을 제공하세요.
"""

class HeadhunterReactAgent:
    """ReAct 패턴 기반 헤드헌터 AI 에이전트"""

    def __init__(self):
        # LLM 초기화
        self.llm = ChatUpstage(
            model="solar-pro",
            temperature=0.1
        )

        # 모든 도구 수집
        self.tools = [
            # 후보자 검색 도구
            search_candidates_by_skills,
            search_candidates_by_location,
            search_candidates_by_salary_range,
            search_candidates_by_work_type,
            search_candidates_by_industry,
            search_candidates_by_availability,
            get_candidate_details,
            complex_candidate_search,
            get_candidate_statistics,

            # 회사 검색 도구
            search_companies_by_name,
            search_companies_by_category,

            # 시장 분석 도구 (RAG)
            search_tech_information,
            search_market_trends,
            search_industry_analysis,
            search_salary_information,
            general_knowledge_search,
            compare_technologies,
            get_knowledge_base_stats,

            # 웹 검색 도구
            web_search_latest_trends,
            search_job_postings,
            search_company_information,
            search_salary_benchmarks,
            search_tech_news,
            search_startup_funding_news
        ]

        # 메모리 체크포인터
        self.memory = MemorySaver()

        # ReAct 에이전트 생성 (state_modifier 제거)
        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
            checkpointer=self.memory
        )

        # 시스템 프롬프트는 invoke 시 추가
        self.system_message = SystemMessage(content=HEADHUNTER_SYSTEM_PROMPT)

    def invoke(self, message: str, thread_id: str = "default") -> Dict[str, Any]:
        """
        에이전트 실행

        Args:
            message: 사용자 메시지
            thread_id: 대화 스레드 ID (세션 관리용)

        Returns:
            에이전트 응답
        """
        config = {"configurable": {"thread_id": thread_id}}

        # 시스템 메시지 + 사용자 메시지
        messages = [self.system_message, HumanMessage(content=message)]

        response = self.agent.invoke(
            {"messages": messages},
            config=config
        )

        return response

    def stream(self, message: str, thread_id: str = "default"):
        """
        스트리밍 응답

        Args:
            message: 사용자 메시지
            thread_id: 대화 스레드 ID

        Yields:
            스트리밍 청크
        """
        config = {"configurable": {"thread_id": thread_id}}

        # 시스템 메시지 + 사용자 메시지
        messages = [self.system_message, HumanMessage(content=message)]

        for chunk in self.agent.stream(
            {"messages": messages},
            config=config,
            stream_mode="values"
        ):
            yield chunk

    def get_chat_history(self, thread_id: str = "default"):
        """
        대화 히스토리 조회

        Args:
            thread_id: 대화 스레드 ID

        Returns:
            대화 히스토리
        """
        config = {"configurable": {"thread_id": thread_id}}
        state = self.agent.get_state(config)
        return state.values.get("messages", [])


# 전역 인스턴스
_react_agent_instance = None

def get_react_agent() -> HeadhunterReactAgent:
    """ReAct 에이전트 싱글톤 인스턴스 반환"""
    global _react_agent_instance
    if _react_agent_instance is None:
        _react_agent_instance = HeadhunterReactAgent()
    return _react_agent_instance


# 간단한 사용 예시
if __name__ == "__main__":
    agent = get_react_agent()

    # 테스트 쿼리
    test_queries = [
        "Python 개발자를 찾고 있어요",
        "데이터 사이언티스트의 평균 연봉이 궁금합니다",
        "최근 AI 개발자 채용 트렌드는 어떤가요?"
    ]

    for query in test_queries:
        print(f"\n질문: {query}")
        print("-" * 50)

        response = agent.invoke(query, thread_id="test-session")

        # 마지막 메시지 출력
        if response["messages"]:
            last_message = response["messages"][-1]
            print(f"답변: {last_message.content}")
