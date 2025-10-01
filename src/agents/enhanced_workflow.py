"""고도화된 헤드헌터 AI 에이전트 LangGraph 워크플로우 - Customer Support Agent 스타일"""

import os
from typing import List, Dict, Any, TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_upstage import ChatUpstage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
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

class HeadhunterAgentState(TypedDict):
    """헤드헌터 에이전트의 상태 정의"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    customer_query: str
    query_type: str  # "candidate_search", "market_analysis", "web_research", "general"
    search_context: Dict[str, Any]
    results: Dict[str, Any]
    next_action: str
    needs_clarification: bool

class EnhancedHeadhunterWorkflow:
    """고도화된 헤드헌터 AI 에이전트 워크플로우"""

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
        self.workflow = self._build_enhanced_workflow()

    def _build_enhanced_workflow(self) -> StateGraph:
        """고도화된 LangGraph 워크플로우 구축"""
        workflow = StateGraph(HeadhunterAgentState)

        # 노드 추가
        workflow.add_node("initial_analysis", self._initial_analysis)
        workflow.add_node("query_classifier", self._classify_query)
        workflow.add_node("context_enricher", self._enrich_context)
        workflow.add_node("candidate_specialist", self._candidate_specialist)
        workflow.add_node("market_specialist", self._market_specialist)
        workflow.add_node("web_researcher", self._web_researcher)
        workflow.add_node("tools", ToolNode(self.all_tools))
        workflow.add_node("result_synthesizer", self._synthesize_results)
        workflow.add_node("quality_checker", self._quality_check)
        workflow.add_node("response_formatter", self._format_response)

        # 시작점 설정
        workflow.set_entry_point("initial_analysis")

        # 워크플로우 엣지 정의
        workflow.add_edge("initial_analysis", "query_classifier")
        workflow.add_edge("query_classifier", "context_enricher")

        # 분류 결과에 따른 라우팅
        workflow.add_conditional_edges(
            "context_enricher",
            self._route_to_specialist,
            {
                "candidate": "candidate_specialist",
                "market": "market_specialist",
                "web": "web_researcher",
                "tools": "tools"
            }
        )

        # 전문가 노드들에서 도구 사용 여부 결정
        for specialist in ["candidate_specialist", "market_specialist", "web_researcher"]:
            workflow.add_conditional_edges(
                specialist,
                self._should_use_tools,
                {
                    "tools": "tools",
                    "synthesize": "result_synthesizer"
                }
            )

        # 도구 사용 후 결과 합성
        workflow.add_edge("tools", "result_synthesizer")

        # 결과 합성 후 품질 검사
        workflow.add_edge("result_synthesizer", "quality_checker")

        # 품질 검사 후 응답 포맷팅 또는 재처리
        workflow.add_conditional_edges(
            "quality_checker",
            self._quality_decision,
            {
                "format": "response_formatter",
                "retry": "context_enricher"
            }
        )

        # 응답 포맷팅 후 종료
        workflow.add_edge("response_formatter", END)

        return workflow

    def _initial_analysis(self, state: HeadhunterAgentState) -> HeadhunterAgentState:
        """초기 분석 - 사용자 쿼리 전처리"""
        last_message = state["messages"][-1]
        user_query = last_message.content

        # 시스템 메시지 추가
        system_message = SystemMessage(content="""
        당신은 전문 헤드헌터 AI 어시스턴트입니다. 다음 역할을 수행합니다:

        1. 인재 검색 및 매칭
        2. 시장 동향 분석
        3. 기술 트렌드 연구
        4. 채용 시장 정보 제공

        항상 정확하고 유용한 정보를 제공하며, 필요시 추가 질문을 통해 더 나은 서비스를 제공합니다.
        """)

        state["messages"] = [system_message] + state["messages"]
        state["customer_query"] = user_query
        state["search_context"] = {}
        state["results"] = {}
        state["needs_clarification"] = False

        return state

    def _classify_query(self, state: HeadhunterAgentState) -> HeadhunterAgentState:
        """쿼리 분류 - 고도화된 분류 로직"""
        user_query = state["customer_query"]

        classification_prompt = f"""
        다음 사용자 질문을 분석하여 가장 적절한 카테고리와 세부 의도를 파악해주세요:

        사용자 질문: {user_query}

        분류 카테고리:
        1. candidate_search - 인재 검색, 후보자 정보, 스킬 매칭, 인재 데이터베이스 조회
        2. market_analysis - 시장 트렌드, 산업 분석, 기술 정보, 급여 분석 (내부 지식 기반)
        3. web_research - 최신 뉴스, 채용공고, 회사 정보, 실시간 트렌드 (웹 검색 필요)
        4. general - 복합적 질문, 상담, 일반적인 헤드헌팅 조언

        응답 형식:
        카테고리: [category]
        의도: [구체적인 의도 설명]
        키워드: [핵심 키워드 3-5개]
        """

        response = self.llm.invoke([HumanMessage(content=classification_prompt)])

        # 응답 파싱 (간단한 파싱 로직)
        response_text = response.content.lower()

        if "candidate" in response_text:
            query_type = "candidate_search"
        elif "market" in response_text:
            query_type = "market_analysis"
        elif "web" in response_text:
            query_type = "web_research"
        else:
            query_type = "general"

        state["query_type"] = query_type
        state["messages"].append(response)

        return state

    def _enrich_context(self, state: HeadhunterAgentState) -> HeadhunterAgentState:
        """컨텍스트 강화 - 쿼리에 필요한 추가 정보 추출"""
        user_query = state["customer_query"]
        query_type = state["query_type"]

        context_prompt = f"""
        사용자 질문에서 중요한 매개변수와 조건을 추출해주세요:

        질문: {user_query}
        분류: {query_type}

        추출할 정보:
        - 기술 스킬 (예: Python, React, AWS)
        - 지역 (예: 서울, 강남구)
        - 경력 년수 (예: 3년 이상)
        - 급여 범위 (예: 7000-10000만원)
        - 산업 분야 (예: Fintech, AI/ML)
        - 근무 형태 (예: 원격, 하이브리드)
        - 기타 조건

        JSON 형식으로 응답해주세요.
        """

        response = self.llm.invoke([HumanMessage(content=context_prompt)])

        # 실제로는 JSON 파싱을 해야 하지만, 여기서는 단순화
        state["search_context"] = {
            "extracted_info": response.content,
            "query_complexity": "medium"
        }

        return state

    def _route_to_specialist(self, state: HeadhunterAgentState) -> str:
        """전문가 라우팅"""
        query_type = state.get("query_type", "general")

        routing_map = {
            "candidate_search": "candidate",
            "market_analysis": "market",
            "web_research": "web"
        }

        return routing_map.get(query_type, "tools")

    def _candidate_specialist(self, state: HeadhunterAgentState) -> HeadhunterAgentState:
        """인재 검색 전문가"""
        specialist_prompt = """
        당신은 인재 검색 전문가입니다. 다음 도구들을 사용하여 정확한 인재 정보를 제공하세요:

        사용 가능한 도구:
        - search_candidates_by_skills: 기술 스킬 기반 검색
        - search_candidates_by_location: 지역 기반 검색
        - search_candidates_by_salary_range: 급여 범위 기반 검색
        - complex_candidate_search: 복합 조건 검색
        - get_candidate_statistics: 통계 정보

        사용자의 요구사항을 정확히 분석하고 가장 적절한 도구를 선택하세요.
        여러 조건이 있다면 complex_candidate_search를 우선 사용하세요.
        """

        user_query = state["customer_query"]
        messages = [HumanMessage(content=specialist_prompt + f"\n\n사용자 질문: {user_query}")]

        response = self.llm_with_tools.invoke(messages)
        state["messages"].append(response)

        return state

    def _market_specialist(self, state: HeadhunterAgentState) -> HeadhunterAgentState:
        """시장 분석 전문가"""
        specialist_prompt = """
        당신은 시장 분석 전문가입니다. 내부 지식 베이스를 활용하여 시장 트렌드와 기술 정보를 제공하세요:

        사용 가능한 도구:
        - search_tech_information: 기술 정보 검색
        - search_market_trends: 시장 트렌드 분석
        - search_industry_analysis: 산업 분석
        - search_salary_information: 급여 정보
        - compare_technologies: 기술 비교

        벡터 검색을 통해 관련성 높은 정보를 찾아 종합적인 분석을 제공하세요.
        """

        user_query = state["customer_query"]
        messages = [HumanMessage(content=specialist_prompt + f"\n\n사용자 질문: {user_query}")]

        response = self.llm_with_tools.invoke(messages)
        state["messages"].append(response)

        return state

    def _web_researcher(self, state: HeadhunterAgentState) -> HeadhunterAgentState:
        """웹 연구 전문가"""
        specialist_prompt = """
        당신은 웹 연구 전문가입니다. Tavily를 통해 최신 정보를 검색하여 제공하세요:

        사용 가능한 도구:
        - web_search_latest_trends: 최신 트렌드 검색
        - search_job_postings: 채용공고 검색
        - search_company_information: 회사 정보 검색
        - search_tech_news: 기술 뉴스 검색
        - search_startup_funding_news: 스타트업 투자 뉴스

        항상 최신이고 신뢰할 수 있는 정보를 웹에서 검색하여 제공하세요.
        """

        user_query = state["customer_query"]
        messages = [HumanMessage(content=specialist_prompt + f"\n\n사용자 질문: {user_query}")]

        response = self.llm_with_tools.invoke(messages)
        state["messages"].append(response)

        return state

    def _should_use_tools(self, state: HeadhunterAgentState) -> str:
        """도구 사용 여부 결정"""
        last_message = state["messages"][-1]

        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools"
        else:
            return "synthesize"

    def _synthesize_results(self, state: HeadhunterAgentState) -> HeadhunterAgentState:
        """결과 합성"""
        synthesis_prompt = """
        수집된 정보를 바탕으로 사용자에게 도움이 되는 종합적인 답변을 생성하세요:

        답변 가이드라인:
        1. 핵심 정보를 명확하게 정리
        2. 구체적인 데이터나 예시 포함
        3. 실행 가능한 권장사항 제시
        4. 전문적이면서도 친근한 톤 유지
        5. 필요시 추가 질문이나 서비스 제안

        이전 대화와 도구 실행 결과를 종합하여 최고 품질의 답변을 제공하세요.
        """

        messages = state["messages"] + [HumanMessage(content=synthesis_prompt)]
        response = self.llm.invoke(messages)

        state["messages"].append(response)
        state["results"]["synthesized_response"] = response.content

        return state

    def _quality_check(self, state: HeadhunterAgentState) -> HeadhunterAgentState:
        """품질 검사"""
        synthesized_response = state["results"].get("synthesized_response", "")

        quality_criteria = [
            len(synthesized_response) > 50,  # 충분한 길이
            "구체적" in synthesized_response or "예시" in synthesized_response,  # 구체성
            any(keyword in synthesized_response for keyword in ["추천", "권장", "제안"])  # 실행가능성
        ]

        quality_score = sum(quality_criteria) / len(quality_criteria)
        state["results"]["quality_score"] = quality_score

        return state

    def _quality_decision(self, state: HeadhunterAgentState) -> str:
        """품질 기반 의사결정"""
        quality_score = state["results"].get("quality_score", 0)

        if quality_score >= 0.7:
            return "format"
        else:
            return "retry"

    def _format_response(self, state: HeadhunterAgentState) -> HeadhunterAgentState:
        """응답 포맷팅"""
        response = state["results"]["synthesized_response"]

        formatted_response = f"""
🤖 **헤드헌터 AI 분석 결과**

{response}

---
📊 **추가 서비스**
- 더 구체적인 인재 검색이 필요하시면 세부 조건을 알려주세요
- 시장 분석 자료가 더 필요하시면 요청해주세요
- 실시간 채용 동향은 웹 검색을 통해 제공 가능합니다

💡 추가 질문이나 상세한 분석이 필요하시면 언제든 말씀해주세요!
        """

        state["messages"].append(AIMessage(content=formatted_response))

        return state

    def get_graph(self):
        """컴파일된 그래프 반환"""
        memory = InMemorySaver()
        return self.workflow.compile(checkpointer=memory)

    def create_react_agent_style(self):
        """React Agent 스타일의 간단한 에이전트 생성"""
        checkpointer = InMemorySaver()

        agent = create_react_agent(
            model=self.llm,
            tools=self.all_tools,
            prompt="당신은 전문 헤드헌터 AI 어시스턴트입니다. 사용 가능한 도구를 활용하여 인재 검색, 시장 분석, 웹 연구를 통해 사용자를 도와주세요.",
            checkpointer=checkpointer
        )

        return agent

# 전역 워크플로우 인스턴스
_enhanced_workflow_instance = None

def get_enhanced_headhunter_workflow():
    """고도화된 워크플로우 인스턴스 반환"""
    global _enhanced_workflow_instance
    if _enhanced_workflow_instance is None:
        _enhanced_workflow_instance = EnhancedHeadhunterWorkflow()
    return _enhanced_workflow_instance

def get_react_headhunter_agent():
    """React 스타일 에이전트 반환"""
    workflow = get_enhanced_headhunter_workflow()
    return workflow.create_react_agent_style()