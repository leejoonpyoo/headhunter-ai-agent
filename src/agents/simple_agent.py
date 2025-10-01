"""간단하고 안정적인 백업 헤드헌터 에이전트"""

import os
from typing import List, Dict, Any
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_upstage import ChatUpstage
from dotenv import load_dotenv

load_dotenv()

class SimpleHeadhunterAgent:
    """간단하고 안정적인 헤드헌터 에이전트 (도구 없이 기본 대화)"""

    def __init__(self):
        self.llm = ChatUpstage(
            model="solar-pro2",
            temperature=0.1
        )

        self.system_prompt = """당신은 전문 헤드헌터 AI 어시스턴트입니다.

주요 역할:
1. 인재 채용 상담 및 조언 제공
2. 시장 동향 및 기술 트렌드 분석
3. 채용 프로세스 가이드
4. 개발자 커리어 상담

항상 전문적이고 도움이 되는 답변을 제공하세요.
구체적인 데이터나 검색이 필요한 경우 그 점을 안내해주세요.

현재 도구 연결이 일시적으로 제한된 상태이므로,
일반적인 상담과 조언 위주로 답변해주시되
필요시 구체적인 검색이나 데이터 조회를 위한
별도 요청을 안내해주세요."""

    def chat(self, user_message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """간단한 채팅 인터페이스"""
        try:
            # 메시지 구성
            messages = [SystemMessage(content=self.system_prompt)]

            # 대화 기록 추가 (최근 5개만)
            if conversation_history:
                recent_history = conversation_history[-5:] if len(conversation_history) > 5 else conversation_history
                for msg in recent_history:
                    if msg["role"] == "user":
                        messages.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "assistant":
                        messages.append(AIMessage(content=msg["content"]))

            # 현재 사용자 메시지 추가
            messages.append(HumanMessage(content=user_message))

            # AI 응답 생성
            response = self.llm.invoke(messages)
            return response.content

        except Exception as e:
            return f"죄송합니다. 일시적인 오류가 발생했습니다: {str(e)}\n\n기본 상담은 가능하니 다시 시도해주세요."

    def get_sample_responses(self) -> Dict[str, str]:
        """샘플 응답들"""
        return {
            "인재검색": "현재 데이터베이스 검색 기능이 일시적으로 제한되어 있습니다. 구체적인 인재 검색을 위해서는 관리자에게 문의해주세요. 하지만 일반적인 채용 전략이나 요구사항 정의에 대해서는 상담해드릴 수 있습니다.",
            "시장동향": "일반적인 개발자 시장 트렌드에 대해서는 상담해드릴 수 있습니다. 최신 데이터나 구체적인 통계가 필요하시면 별도 검색을 요청해주세요.",
            "기술상담": "기술 스택 선택, 커리어 패스, 채용 요구사항 등에 대해 상담해드릴 수 있습니다."
        }

# 전역 인스턴스
_simple_agent_instance = None

def get_simple_headhunter_agent():
    """간단한 에이전트 인스턴스 반환"""
    global _simple_agent_instance
    if _simple_agent_instance is None:
        _simple_agent_instance = SimpleHeadhunterAgent()
    return _simple_agent_instance