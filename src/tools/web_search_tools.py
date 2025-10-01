"""외부 웹 검색 도구들 (Tavily)"""

import os
from typing import List, Dict, Any
from langchain_core.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

# Tavily 클라이언트 초기화
tavily_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

@tool
def web_search_latest_trends(query: str, max_results: int = 3, include_domains: List[str] = None) -> List[Dict[str, Any]]:
    """
    최신 채용/개발자 트렌드 웹 검색 도구

    Args:
        query: 검색 쿼리 (예: "2024 개발자 채용 트렌드", "AI 엔지니어 시장 동향")
        max_results: 최대 검색 결과 수
        include_domains: 포함할 도메인 리스트 (선택사항)

    Returns:
        최신 웹 검색 결과
    """
    try:
        # Tavily 검색 실행
        search_params = {
            "query": query,
            "max_results": max_results,
            "search_depth": "advanced",
            "include_answer": True
        }

        if include_domains:
            search_params["include_domains"] = include_domains

        results = tavily_client.search(**search_params)

        # 결과 포맷팅
        formatted_results = []
        for result in results.get('results', []):
            formatted_results.append({
                "title": result.get('title', ''),
                "content": result.get('content', ''),
                "url": result.get('url', ''),
                "score": result.get('score', 0),
                "published_date": result.get('published_date', '')
            })

        return {
            "success": True,
            "query": query,
            "count": len(formatted_results),
            "results": formatted_results,
            "answer": results.get('answer', ''),
            "message": f"'{query}'에 대한 최신 웹 검색 결과 {len(formatted_results)}건을 찾았습니다."
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "웹 검색 중 오류가 발생했습니다."
        }

@tool
def search_job_postings(position: str, location: str = "한국", max_results: int = 5) -> List[Dict[str, Any]]:
    """
    채용공고 검색 도구

    Args:
        position: 검색할 직무 (예: "Python 개발자", "프론트엔드 개발자")
        location: 지역 (기본값: "한국")
        max_results: 최대 검색 결과 수

    Returns:
        관련 채용공고 정보
    """
    try:
        query = f"{position} 채용 {location} 개발자 채용공고"

        results = tavily_client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
            include_domains=["saramin.co.kr", "jobkorea.co.kr", "wanted.co.kr", "programmers.co.kr"]
        )

        formatted_results = []
        for result in results.get('results', []):
            formatted_results.append({
                "title": result.get('title', ''),
                "content": result.get('content', ''),
                "url": result.get('url', ''),
                "score": result.get('score', 0)
            })

        return {
            "success": True,
            "position": position,
            "location": location,
            "count": len(formatted_results),
            "job_postings": formatted_results,
            "message": f"{location}의 '{position}' 채용공고 {len(formatted_results)}건을 찾았습니다."
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "채용공고 검색 중 오류가 발생했습니다."
        }

@tool
def search_company_information(company_name: str, max_results: int = 3) -> List[Dict[str, Any]]:
    """
    회사 정보 검색 도구

    Args:
        company_name: 검색할 회사명
        max_results: 최대 검색 결과 수

    Returns:
        회사 정보 및 채용 현황
    """
    try:
        query = f"{company_name} 회사 정보 채용 개발자 복리후생"

        results = tavily_client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced"
        )

        formatted_results = []
        for result in results.get('results', []):
            formatted_results.append({
                "title": result.get('title', ''),
                "content": result.get('content', ''),
                "url": result.get('url', ''),
                "score": result.get('score', 0)
            })

        return {
            "success": True,
            "company": company_name,
            "count": len(formatted_results),
            "company_info": formatted_results,
            "message": f"'{company_name}' 회사 정보 {len(formatted_results)}건을 찾았습니다."
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "회사 정보 검색 중 오류가 발생했습니다."
        }

@tool
def search_salary_benchmarks(position: str, location: str = "한국", max_results: int = 3) -> List[Dict[str, Any]]:
    """
    급여 벤치마크 웹 검색 도구

    Args:
        position: 직무명 (예: "시니어 개발자", "데이터 사이언티스트")
        location: 지역 (기본값: "한국")
        max_results: 최대 검색 결과 수

    Returns:
        최신 급여 벤치마크 정보
    """
    try:
        query = f"{position} 연봉 급여 {location} 2024"

        results = tavily_client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced"
        )

        formatted_results = []
        for result in results.get('results', []):
            formatted_results.append({
                "title": result.get('title', ''),
                "content": result.get('content', ''),
                "url": result.get('url', ''),
                "score": result.get('score', 0)
            })

        return {
            "success": True,
            "position": position,
            "location": location,
            "count": len(formatted_results),
            "salary_benchmarks": formatted_results,
            "message": f"{location}의 '{position}' 급여 정보 {len(formatted_results)}건을 찾았습니다."
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "급여 벤치마크 검색 중 오류가 발생했습니다."
        }

@tool
def search_tech_news(technology: str, max_results: int = 3) -> List[Dict[str, Any]]:
    """
    기술 관련 최신 뉴스 검색 도구

    Args:
        technology: 기술명 (예: "Python", "React", "AI", "블록체인")
        max_results: 최대 검색 결과 수

    Returns:
        해당 기술의 최신 뉴스
    """
    try:
        query = f"{technology} 기술 뉴스 트렌드 2024"

        results = tavily_client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
            include_domains=["techcrunch.com", "zdnet.co.kr", "bloter.net", "itworld.co.kr"]
        )

        formatted_results = []
        for result in results.get('results', []):
            formatted_results.append({
                "title": result.get('title', ''),
                "content": result.get('content', ''),
                "url": result.get('url', ''),
                "score": result.get('score', 0),
                "published_date": result.get('published_date', '')
            })

        return {
            "success": True,
            "technology": technology,
            "count": len(formatted_results),
            "tech_news": formatted_results,
            "message": f"'{technology}' 관련 최신 뉴스 {len(formatted_results)}건을 찾았습니다."
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "기술 뉴스 검색 중 오류가 발생했습니다."
        }

@tool
def search_startup_funding_news(max_results: int = 3) -> List[Dict[str, Any]]:
    """
    스타트업 투자 및 채용 뉴스 검색 도구

    Args:
        max_results: 최대 검색 결과 수

    Returns:
        스타트업 투자 및 채용 관련 최신 뉴스
    """
    try:
        query = "스타트업 투자 채용 개발자 2024"

        results = tavily_client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced"
        )

        formatted_results = []
        for result in results.get('results', []):
            formatted_results.append({
                "title": result.get('title', ''),
                "content": result.get('content', ''),
                "url": result.get('url', ''),
                "score": result.get('score', 0),
                "published_date": result.get('published_date', '')
            })

        return {
            "success": True,
            "count": len(formatted_results),
            "startup_news": formatted_results,
            "message": f"스타트업 투자/채용 뉴스 {len(formatted_results)}건을 찾았습니다."
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "스타트업 뉴스 검색 중 오류가 발생했습니다."
        }