"""간단한 헤드헌터 워크플로우 테스트"""

import os
import sys
from langchain_core.messages import HumanMessage

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def test_basic_workflow():
    """기본 워크플로우 테스트"""
    print("=== 헤드헌터 AI 워크플로우 테스트 ===")

    try:
        from src.agents.workflow import get_headhunter_workflow

        print("워크플로우 초기화 중...")
        workflow_instance = get_headhunter_workflow()
        graph = workflow_instance.get_graph()

        print("워크플로우 초기화 성공!")

        # 간단한 테스트 쿼리
        test_query = "Python 개발자가 몇 명 등록되어 있어?"
        print(f"테스트 쿼리: {test_query}")

        result = graph.invoke(
            {"messages": [HumanMessage(content=test_query)]},
            config={"configurable": {"thread_id": "test"}}
        )

        if result and "messages" in result:
            response = result["messages"][-1].content
            print(f"AI 응답: {response[:200]}...")
            print("테스트 성공!")
        else:
            print("응답을 받지 못했습니다.")

    except Exception as e:
        print(f"오류 발생: {str(e)}")

def test_enhanced_workflow():
    """고도화된 워크플로우 테스트"""
    print("\n=== 고도화된 워크플로우 테스트 ===")

    try:
        from src.agents.enhanced_workflow import get_enhanced_headhunter_workflow

        print("고도화된 워크플로우 초기화 중...")
        workflow_instance = get_enhanced_headhunter_workflow()
        graph = workflow_instance.get_graph()

        print("고도화된 워크플로우 초기화 성공!")

        # 테스트 쿼리
        test_query = "최근 AI 개발자 시장 동향이 어때?"
        print(f"테스트 쿼리: {test_query}")

        result = graph.invoke(
            {"messages": [HumanMessage(content=test_query)]},
            config={"configurable": {"thread_id": "enhanced_test"}}
        )

        if result and "messages" in result:
            response = result["messages"][-1].content
            print(f"AI 응답: {response[:200]}...")
            print("고도화된 워크플로우 테스트 성공!")
        else:
            print("응답을 받지 못했습니다.")

    except Exception as e:
        print(f"고도화된 워크플로우 오류: {str(e)}")

def test_database_graceful_handling():
    """데이터베이스 우아한 오류 처리 테스트"""
    print("\n=== 데이터베이스 오류 처리 테스트 ===")

    try:
        from src.database.connection import is_db_available
        from src.tools.candidate_tools import get_candidate_statistics

        print(f"데이터베이스 연결 상태: {is_db_available()}")

        # 통계 도구 테스트 (DB 연결이 안되어도 우아하게 처리되어야 함)
        result = get_candidate_statistics.invoke({})
        print(f"통계 조회 결과: {result}")

        if result.get("success") == False:
            print("데이터베이스 연결 실패를 우아하게 처리했습니다!")
        else:
            print("데이터베이스 연결 성공!")

    except Exception as e:
        print(f"데이터베이스 테스트 오류: {str(e)}")

if __name__ == "__main__":
    # 기본 워크플로우 테스트
    test_basic_workflow()

    # 고도화된 워크플로우 테스트
    test_enhanced_workflow()

    # 데이터베이스 오류 처리 테스트
    test_database_graceful_handling()

    print("\n모든 테스트가 완료되었습니다!")