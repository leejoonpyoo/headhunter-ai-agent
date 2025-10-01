"""헤드헌터 AI 에이전트 LangGraph 워크플로우"""

import os
from typing import List, Dict, Any, TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_upstage import ChatUpstage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

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
    get_candidate_statistics
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

def add_messages(left: List[BaseMessage], right: List[BaseMessage]) -> List[BaseMessage]:
    """Simple message concatenation function"""
    return left + right

class HeadhunterState(TypedDict):
    """헤드헌터 에이전트 상태"""
    messages: Annotated[List[BaseMessage], add_messages]
    query_type: str  # "candidate_search", "market_research", "tech_info", "web_search", "general"
    search_results: Dict[str, Any]
    next_action: str

class HeadhunterWorkflow:
    """헤드헌터 AI 에이전트 워크플로우 클래스"""

    def __init__(self):
        # LLM 초기화
        self.llm = ChatUpstage(
            model="solar-pro2",
            temperature=0
        )

        # 도구들 설정
        self.candidate_tools = [
            search_candidates_by_skills,
            search_candidates_by_location,
            search_candidates_by_salary_range,
            search_candidates_by_work_type,
            search_candidates_by_industry,
            search_candidates_by_availability,
            get_candidate_details,
            complex_candidate_search,
            get_candidate_statistics
        ]

        self.market_tools = [
            search_tech_information,
            search_market_trends,
            search_industry_analysis,
            search_salary_information,
            general_knowledge_search,
            compare_technologies,
            get_knowledge_base_stats
        ]

        self.web_tools = [
            web_search_latest_trends,
            search_job_postings,
            search_company_information,
            search_salary_benchmarks,
            search_tech_news,
            search_startup_funding_news
        ]

        # 모든 도구 결합
        self.all_tools = self.candidate_tools + self.market_tools + self.web_tools

        # LLM에 도구 바인딩
        self.llm_with_tools = self.llm.bind_tools(self.all_tools)

        # 워크플로우 구축
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> StateGraph:
        """LangGraph 워크플로우 구축"""
        workflow = StateGraph(HeadhunterState)

        # 노드 추가
        workflow.add_node("classifier", self._classify_query)
        workflow.add_node("candidate_agent", self._candidate_agent)
        workflow.add_node("market_agent", self._market_agent)
        workflow.add_node("web_agent", self._web_agent)
        workflow.add_node("general_agent", self._general_agent)
        workflow.add_node("tools", ToolNode(self.all_tools))
        workflow.add_node("synthesizer", self._synthesize_response)

        # 시작점 설정
        workflow.set_entry_point("classifier")

        # 분류기에서 각 에이전트로의 라우팅
        workflow.add_conditional_edges(
            "classifier",
            self._route_to_agent,
            {
                "candidate": "candidate_agent",
                "market": "market_agent",
                "web": "web_agent",
                "general": "general_agent"
            }
        )

        # 각 에이전트에서 도구 또는 응답 생성으로
        for agent in ["candidate_agent", "market_agent", "web_agent", "general_agent"]:
            workflow.add_conditional_edges(
                agent,
                self._should_use_tools,
                {
                    "tools": "tools",
                    "synthesize": "synthesizer"
                }
            )

        # 도구 사용 후 응답 생성
        workflow.add_edge("tools", "synthesizer")

        # 응답 생성 후 종료
        workflow.add_edge("synthesizer", END)

        return workflow

    def _classify_query(self, state: HeadhunterState) -> HeadhunterState:
        """쿼리 분류"""
        last_message = state["messages"][-1]
        user_query = last_message.content

        classification_prompt = f"""
        다음 사용자 질문을 분석하여 적절한 카테고리로 분류해주세요:

        사용자 질문: {user_query}

        카테고리:
        1. candidate - 인재 검색, 후보자 정보, 스킬 매칭 관련
        2. market - 시장 트렌드, 산업 분석, 기술 정보 관련 (내부 지식)
        3. web - 최신 뉴스, 채용공고, 회사 정보 등 실시간 정보 필요
        4. general - 일반적인 상담, 복합적인 질문

        응답은 카테고리명만 반환하세요.
        """

        response = self.llm.invoke(classification_prompt)
        query_type = response.content.strip().lower()

        state["query_type"] = query_type
        return state

    def _route_to_agent(self, state: HeadhunterState) -> str:
        """에이전트 라우팅"""
        query_type = state.get("query_type", "general")

        if "candidate" in query_type:
            return "candidate"
        elif "market" in query_type:
            return "market"
        elif "web" in query_type:
            return "web"
        else:
            return "general"

    def _candidate_agent(self, state: HeadhunterState) -> HeadhunterState:
        """인재 검색 전담 에이전트"""
        candidate_prompt = """
        당신은 인재 검색 전문 에이전트입니다. 사용자의 요청에 따라 적절한 인재 검색 도구를 사용하여 정확한 정보를 제공하세요.

        사용 가능한 도구들:
        - search_candidates_by_skills: 기술 스킬 기반 검색
        - search_candidates_by_location: 지역 기반 검색
        - search_candidates_by_salary_range: 급여 범위 기반 검색
        - search_candidates_by_work_type: 근무 형태 기반 검색
        - search_candidates_by_industry: 산업 분야 기반 검색
        - search_candidates_by_availability: 구직 상태 기반 검색
        - complex_candidate_search: 복합 조건 검색
        - get_candidate_details: 특정 인재 상세 정보
        - get_candidate_statistics: 전체 통계

        항상 도구를 사용하여 정확한 데이터를 제공하세요.
        """

        last_message = state["messages"][-1]
        messages = [HumanMessage(content=candidate_prompt + "\n\n사용자 질문: " + last_message.content)]

        response = self.llm_with_tools.invoke(messages)
        state["messages"].append(response)

        return state

    def _market_agent(self, state: HeadhunterState) -> HeadhunterState:
        """시장 정보 전담 에이전트"""
        market_prompt = """
        당신은 시장 분석 및 기술 정보 전문 에이전트입니다. 내부 지식 베이스를 활용하여 시장 트렌드, 기술 정보, 산업 분석을 제공하세요.

        사용 가능한 도구들:
        - search_tech_information: 기술 정보 검색
        - search_market_trends: 시장 트렌드 검색
        - search_industry_analysis: 산업 분석 검색
        - search_salary_information: 급여 정보 검색
        - general_knowledge_search: 일반 지식 검색
        - compare_technologies: 기술 비교
        - get_knowledge_base_stats: 지식 베이스 통계

        벡터 검색을 통해 관련성 높은 정보를 찾아서 제공하세요.
        """

        last_message = state["messages"][-1]
        messages = [HumanMessage(content=market_prompt + "\n\n사용자 질문: " + last_message.content)]

        response = self.llm_with_tools.invoke(messages)
        state["messages"].append(response)

        return state

    def _web_agent(self, state: HeadhunterState) -> HeadhunterState:
        """웹 검색 전담 에이전트"""
        web_prompt = """
        당신은 실시간 웹 정보 검색 전문 에이전트입니다. Tavily를 통해 최신 정보를 검색하여 제공하세요.

        사용 가능한 도구들:
        - web_search_latest_trends: 최신 트렌드 검색
        - search_job_postings: 채용공고 검색
        - search_company_information: 회사 정보 검색
        - search_salary_benchmarks: 급여 벤치마크 검색
        - search_tech_news: 기술 뉴스 검색
        - search_startup_funding_news: 스타트업 투자 뉴스 검색

        항상 최신 정보를 웹에서 검색하여 제공하세요.
        """

        last_message = state["messages"][-1]
        messages = [HumanMessage(content=web_prompt + "\n\n사용자 질문: " + last_message.content)]

        response = self.llm_with_tools.invoke(messages)
        state["messages"].append(response)

        return state

    def _general_agent(self, state: HeadhunterState) -> HeadhunterState:
        """일반 상담 에이전트"""
        general_prompt = """
        당신은 헤드헌터 AI 어시스턴트입니다. 사용자의 질문에 따라 적절한 도구를 선택하여 종합적인 답변을 제공하세요.

        복합적인 질문의 경우 여러 도구를 조합하여 사용할 수 있습니다:
        - 인재 정보가 필요하면 candidate 도구들을 사용
        - 시장 정보가 필요하면 market 도구들을 사용
        - 최신 정보가 필요하면 web 도구들을 사용

        항상 사용자에게 도움이 되는 포괄적인 답변을 제공하세요.
        """

        last_message = state["messages"][-1]
        messages = [HumanMessage(content=general_prompt + "\n\n사용자 질문: " + last_message.content)]

        response = self.llm_with_tools.invoke(messages)
        state["messages"].append(response)

        return state

    def _should_use_tools(self, state: HeadhunterState) -> str:
        """도구 사용 여부 결정"""
        last_message = state["messages"][-1]

        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools"
        else:
            return "synthesize"

    def _synthesize_response(self, state: HeadhunterState) -> HeadhunterState:
        """최종 응답 생성"""
        synthesis_prompt = """
        앞서 수집한 정보를 바탕으로 사용자에게 도움이 되는 최종 답변을 생성하세요.

        답변 가이드라인:
        1. 핵심 정보를 명확하게 정리
        2. 구체적인 데이터나 예시 포함
        3. 추가 조치나 권장사항 제시
        4. 친근하고 전문적인 톤 유지

        이전 대화 내용을 참고하여 종합적인 답변을 제공하세요.
        """

        messages = state["messages"] + [HumanMessage(content=synthesis_prompt)]
        response = self.llm.invoke(messages)

        state["messages"].append(response)
        return state

    def get_graph(self):
        """컴파일된 그래프 반환"""
        memory = InMemorySaver()
        return self.workflow.compile(checkpointer=memory)

# 전역 워크플로우 인스턴스
_workflow_instance = None

def get_headhunter_workflow():
    """전역 워크플로우 인스턴스 반환"""
    global _workflow_instance
    if _workflow_instance is None:
        _workflow_instance = HeadhunterWorkflow()
    return _workflow_instance