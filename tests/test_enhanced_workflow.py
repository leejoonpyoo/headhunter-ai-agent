"""고도화된 헤드헌터 워크플로우 테스트 스크립트"""

import os
import sys
from langchain_core.messages import HumanMessage

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from src.agents.enhanced_workflow import get_enhanced_headhunter_workflow, get_react_headhunter_agent

def test_enhanced_workflow():
    """고도화된 워크플로우 테스트"""
    print("🚀 고도화된 헤드헌터 워크플로우 테스트 시작")
    print("=" * 60)

    try:
        # 워크플로우 인스턴스 생성
        workflow_instance = get_enhanced_headhunter_workflow()
        graph = workflow_instance.get_graph()

        print("✅ 워크플로우 초기화 성공")

        # 테스트 쿼리들
        test_queries = [
            "Python 개발자 5년 이상 경력자를 찾아줘",
            "AI 개발자 시장 트렌드가 어떻게 되고 있어?",
            "최근 스타트업 채용 동향을 웹에서 찾아줘"
        ]

        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 테스트 {i}: {query}")
            print("-" * 40)

            try:
                # 워크플로우 실행
                result = graph.invoke(
                    {"messages": [HumanMessage(content=query)]},
                    config={"configurable": {"thread_id": f"test_thread_{i}"}}
                )

                # 결과 출력
                if result and "messages" in result:
                    last_message = result["messages"][-1]
                    print(f"🤖 AI 응답: {last_message.content[:200]}...")
                    print("✅ 테스트 성공")
                else:
                    print("❌ 응답을 받지 못했습니다")

            except Exception as e:
                print(f"❌ 테스트 실패: {str(e)}")

    except Exception as e:
        print(f"❌ 워크플로우 초기화 실패: {str(e)}")

def test_react_agent():
    """React Agent 스타일 테스트"""
    print("\n🤖 React Agent 스타일 테스트 시작")
    print("=" * 60)

    try:
        # React Agent 생성
        agent = get_react_headhunter_agent()
        print("✅ React Agent 초기화 성공")

        # 간단한 테스트
        test_query = "인재 데이터베이스에 몇 명의 개발자가 등록되어 있어?"
        print(f"\n🔍 테스트 쿼리: {test_query}")

        result = agent.invoke(
            {"messages": [HumanMessage(content=test_query)]},
            config={"configurable": {"thread_id": "react_test"}}
        )

        if result and "messages" in result:
            last_message = result["messages"][-1]
            print(f"🤖 React Agent 응답: {last_message.content[:200]}...")
            print("✅ React Agent 테스트 성공")
        else:
            print("❌ React Agent 응답을 받지 못했습니다")

    except Exception as e:
        print(f"❌ React Agent 테스트 실패: {str(e)}")

def interactive_chat():
    """대화형 채팅 테스트"""
    print("\n💬 대화형 채팅 테스트 (quit 입력시 종료)")
    print("=" * 60)

    try:
        # 워크플로우 또는 React Agent 선택
        choice = input("워크플로우(1) 또는 React Agent(2)를 선택하세요: ").strip()

        if choice == "1":
            workflow_instance = get_enhanced_headhunter_workflow()
            agent = workflow_instance.get_graph()
            agent_type = "Enhanced Workflow"
        elif choice == "2":
            agent = get_react_headhunter_agent()
            agent_type = "React Agent"
        else:
            print("❌ 잘못된 선택입니다")
            return

        print(f"✅ {agent_type} 초기화 성공")
        print("💡 채팅을 시작하세요! (quit 입력시 종료)")

        thread_id = "interactive_chat"
        message_count = 0

        while True:
            user_input = input("\n👤 You: ").strip()

            if user_input.lower() in ['quit', 'exit', '종료']:
                print("👋 채팅을 종료합니다.")
                break

            if not user_input:
                continue

            try:
                message_count += 1
                result = agent.invoke(
                    {"messages": [HumanMessage(content=user_input)]},
                    config={"configurable": {"thread_id": thread_id}}
                )

                if result and "messages" in result:
                    last_message = result["messages"][-1]
                    print(f"\n🤖 AI: {last_message.content}")
                else:
                    print("❌ 응답을 받지 못했습니다")

            except Exception as e:
                print(f"❌ 오류 발생: {str(e)}")

    except Exception as e:
        print(f"❌ 채팅 초기화 실패: {str(e)}")

if __name__ == "__main__":
    print("🎯 헤드헌터 AI 에이전트 테스트 프로그램")
    print("=" * 60)

    while True:
        print("\n선택하세요:")
        print("1. 고도화된 워크플로우 테스트")
        print("2. React Agent 테스트")
        print("3. 대화형 채팅 테스트")
        print("4. 종료")

        choice = input("\n번호를 입력하세요: ").strip()

        if choice == "1":
            test_enhanced_workflow()
        elif choice == "2":
            test_react_agent()
        elif choice == "3":
            interactive_chat()
        elif choice == "4":
            print("👋 프로그램을 종료합니다.")
            break
        else:
            print("❌ 잘못된 선택입니다. 다시 시도해주세요.")