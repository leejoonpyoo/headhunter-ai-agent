"""외부 웹 검색 도구들 (Tavily)

이 모듈은 Tavily API를 활용한 채용/개발자 트렌드 검색 도구를 제공합니다.
LangChain의 @tool 데코레이터를 사용하여 LLM 에이전트가 활용할 수 있는
구조화된 도구로 구현되었습니다.
"""

import os
from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

# Tavily 클라이언트 초기화
tavily_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

@tool(parse_docstring=True)
def web_search_latest_trends(
    query: str, 
    max_results: int = 3, 
    include_domains: Optional[List[str]] = None
) -> Dict[str, Any]:
    """최신 채용 및 개발자 트렌드를 웹에서 검색합니다.
    
    이 도구는 Tavily의 고급 검색 기능을 사용하여 최신 기술 트렌드, 
    채용 동향, 개발자 시장 정보를 찾습니다. 검색 결과는 관련성 점수와 
    함께 제공되며, AI가 생성한 요약 답변도 포함됩니다.
    
    사용 시점:
    - 최신 기술 트렌드나 개발자 채용 시장 동향을 파악할 때
    - 특정 기술 스택이나 직무의 최신 정보가 필요할 때
    - 산업 전반의 개발자 관련 뉴스를 검색할 때
    
    Args:
        query: 검색할 키워드 또는 질문. 예: "2024 AI 개발자 트렌드", 
            "풀스택 개발자 채용 동향"
        max_results: 반환할 최대 검색 결과 수 (기본값: 3, 권장 범위: 1-5)
        include_domains: 검색 범위를 특정 도메인으로 제한. 예: ["techcrunch.com", 
            "zdnet.co.kr"]. None인 경우 모든 도메인 검색
    
    Returns:
        검색 결과를 포함한 딕셔너리:
            - success (bool): 검색 성공 여부
            - query (str): 실행된 검색 쿼리
            - count (int): 반환된 결과 수
            - results (List[Dict]): 검색 결과 리스트. 각 결과는 다음 포함:
                - title (str): 문서 제목
                - content (str): 문서 내용 요약
                - url (str): 원본 URL
                - score (float): 관련성 점수 (0-1)
                - published_date (str): 발행일 (가능한 경우)
            - answer (str): AI가 생성한 종합 답변
            - message (str): 검색 결과 요약 메시지
    
    Raises:
        Exception: Tavily API 호출 실패 시. 오류 정보는 반환 딕셔너리의 
            'error' 키에 포함됩니다.
    
    Examples:
        >>> result = web_search_latest_trends("AI 개발자 연봉 트렌드 2024")
        >>> print(result['answer'])
        >>> for item in result['results']:
        ...     print(f"{item['title']}: {item['url']}")
        
        >>> # 특정 도메인만 검색
        >>> result = web_search_latest_trends(
        ...     "백엔드 개발자 채용",
        ...     max_results=5,
        ...     include_domains=["wanted.co.kr", "jobkorea.co.kr"]
        ... )
    """
    try:
        search_params = {
            "query": query,
            "max_results": max_results,
            "search_depth": "advanced",
            "include_answer": True
        }

        if include_domains:
            search_params["include_domains"] = include_domains

        results = tavily_client.search(**search_params)

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

@tool(parse_docstring=True)
def search_job_postings(
    position: str, 
    location: str = "한국", 
    max_results: int = 5
) -> Dict[str, Any]:
    """특정 포지션의 채용공고를 검색합니다.
    
    한국 주요 채용 플랫폼(사람인, 잡코리아, 원티드, 프로그래머스)에서
    개발자 채용공고를 검색합니다. 포지션명과 지역을 기반으로 최신 
    채용 정보를 수집합니다.
    
    사용 시점:
    - 특정 개발 포지션의 채용 공고를 찾을 때
    - 지역별 채용 시장 현황을 파악할 때
    - 실제 채용 중인 회사 정보를 확인할 때
    
    Args:
        position: 검색할 직무/포지션. 예: "백엔드 개발자", "프론트엔드 개발자",
            "데이터 사이언티스트", "DevOps 엔지니어"
        location: 검색할 지역 (기본값: "한국"). 예: "서울", "판교", "부산"
        max_results: 반환할 최대 채용공고 수 (기본값: 5, 권장 범위: 3-10)
    
    Returns:
        채용공고 검색 결과 딕셔너리:
            - success (bool): 검색 성공 여부
            - position (str): 검색한 포지션
            - location (str): 검색한 지역
            - count (int): 찾은 채용공고 수
            - job_postings (List[Dict]): 채용공고 리스트. 각 공고는 다음 포함:
                - title (str): 채용공고 제목
                - content (str): 채용공고 내용 요약
                - url (str): 채용공고 상세 페이지 URL
                - score (float): 검색 쿼리와의 관련성 점수
            - message (str): 검색 결과 요약 메시지
    
    Raises:
        Exception: 채용공고 검색 실패 시. 오류는 반환 딕셔너리의 
            'error' 키에 포함됩니다.
    
    Examples:
        >>> postings = search_job_postings("풀스택 개발자", "서울")
        >>> for job in postings['job_postings']:
        ...     print(f"{job['title']}\n{job['url']}\n")
        
        >>> # 더 많은 결과 검색
        >>> postings = search_job_postings("AI 엔지니어", max_results=10)
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

@tool(parse_docstring=True)
def search_company_information(
    company_name: str, 
    max_results: int = 3
) -> Dict[str, Any]:
    """특정 회사의 정보를 검색합니다.
    
    회사의 일반 정보, 채용 현황, 복리후생, 개발 문화 등을 검색합니다.
    스타트업부터 대기업까지 다양한 회사의 정보를 수집할 수 있습니다.
    
    사용 시점:
    - 입사를 고려하는 회사에 대한 정보가 필요할 때
    - 회사의 개발 문화나 기술 스택을 파악할 때
    - 복리후생이나 근무 환경 정보를 찾을 때
    - 회사의 최근 소식이나 투자 현황을 알아볼 때
    
    Args:
        company_name: 검색할 회사명. 예: "카카오", "네이버", "토스", 
            "배달의민족", "당근마켓"
        max_results: 반환할 최대 검색 결과 수 (기본값: 3, 권장 범위: 2-5)
    
    Returns:
        회사 정보 검색 결과 딕셔너리:
            - success (bool): 검색 성공 여부
            - company (str): 검색한 회사명
            - count (int): 찾은 정보 수
            - company_info (List[Dict]): 회사 정보 리스트. 각 정보는 다음 포함:
                - title (str): 정보 제목
                - content (str): 회사 정보 내용 요약
                - url (str): 원본 정보 URL
                - score (float): 검색 쿼리와의 관련성 점수
            - message (str): 검색 결과 요약 메시지
    
    Raises:
        Exception: 회사 정보 검색 실패 시. 오류는 반환 딕셔너리의 
            'error' 키에 포함됩니다.
    
    Examples:
        >>> info = search_company_information("토스")
        >>> for item in info['company_info']:
        ...     print(f"{item['title']}")
        ...     print(f"내용: {item['content'][:100]}...")
        ...     print(f"출처: {item['url']}\n")
        
        >>> # 더 많은 정보 수집
        >>> info = search_company_information("당근마켓", max_results=5)
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

@tool(parse_docstring=True)
def search_salary_benchmarks(
    position: str, 
    location: str = "한국", 
    max_results: int = 3
) -> Dict[str, Any]:
    """특정 포지션의 급여 벤치마크 정보를 검색합니다.
    
    개발자 포지션의 평균 연봉, 경력별 급여 수준, 연봉 협상 팁 등을 
    검색합니다. 최신 연봉 데이터를 기반으로 현실적인 급여 정보를 제공합니다.
    
    사용 시점:
    - 특정 포지션의 시장 급여 수준을 파악할 때
    - 연봉 협상을 준비할 때
    - 경력별 급여 성장 곡선을 이해할 때
    - 다른 지역과의 급여 차이를 비교할 때
    
    Args:
        position: 급여 정보를 검색할 직무. 예: "시니어 백엔드 개발자",
            "주니어 프론트엔드 개발자", "ML 엔지니어 3년차"
        location: 검색할 지역 (기본값: "한국"). 예: "서울", "판교", "미국"
        max_results: 반환할 최대 검색 결과 수 (기본값: 3, 권장 범위: 2-5)
    
    Returns:
        급여 정보 검색 결과 딕셔너리:
            - success (bool): 검색 성공 여부
            - position (str): 검색한 포지션
            - location (str): 검색한 지역
            - count (int): 찾은 급여 정보 수
            - salary_benchmarks (List[Dict]): 급여 정보 리스트. 각 정보는 다음 포함:
                - title (str): 급여 정보 제목
                - content (str): 급여 정보 내용 (평균 연봉, 범위 등)
                - url (str): 원본 정보 URL
                - score (float): 검색 쿼리와의 관련성 점수
            - message (str): 검색 결과 요약 메시지
    
    Raises:
        Exception: 급여 정보 검색 실패 시. 오류는 반환 딕셔너리의 
            'error' 키에 포함됩니다.
    
    Examples:
        >>> salary = search_salary_benchmarks("백엔드 개발자 5년차")
        >>> for info in salary['salary_benchmarks']:
        ...     print(f"{info['title']}")
        ...     print(f"{info['content']}\n")
        
        >>> # 지역 비교
        >>> seoul = search_salary_benchmarks("프론트엔드 개발자", "서울")
        >>> pangyo = search_salary_benchmarks("프론트엔드 개발자", "판교")
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

@tool(parse_docstring=True)
def search_tech_news(
    technology: str, 
    max_results: int = 3
) -> Dict[str, Any]:
    """특정 기술에 관한 최신 뉴스와 트렌드를 검색합니다.
    
    기술 관련 뉴스, 업데이트, 트렌드, 커뮤니티 반응 등을 주요 IT 미디어에서
    검색합니다. 기술 선택이나 학습 방향 결정에 도움이 되는 정보를 제공합니다.
    
    사용 시점:
    - 새로운 기술을 학습하기 전에 최신 동향을 파악할 때
    - 기술 스택 선택을 위한 정보가 필요할 때
    - 특정 기술의 산업 채택 현황을 알아볼 때
    - 최신 버전이나 중요 업데이트 정보를 확인할 때
    
    Args:
        technology: 검색할 기술명. 예: "React", "Python 3.12", "Kubernetes",
            "GPT-4", "Next.js 14", "TypeScript 5.0"
        max_results: 반환할 최대 뉴스 수 (기본값: 3, 권장 범위: 2-5)
    
    Returns:
        기술 뉴스 검색 결과 딕셔너리:
            - success (bool): 검색 성공 여부
            - technology (str): 검색한 기술명
            - count (int): 찾은 뉴스 수
            - tech_news (List[Dict]): 뉴스 리스트. 각 뉴스는 다음 포함:
                - title (str): 뉴스 제목
                - content (str): 뉴스 내용 요약
                - url (str): 원본 뉴스 URL
                - score (float): 검색 쿼리와의 관련성 점수
                - published_date (str): 발행일 (가능한 경우)
            - message (str): 검색 결과 요약 메시지
    
    Raises:
        Exception: 기술 뉴스 검색 실패 시. 오류는 반환 딕셔너리의 
            'error' 키에 포함됩니다.
    
    Examples:
        >>> news = search_tech_news("React 19")
        >>> for article in news['tech_news']:
        ...     print(f"[{article['published_date']}] {article['title']}")
        ...     print(f"{article['url']}\n")
        
        >>> # 여러 기술 비교
        >>> react_news = search_tech_news("React")
        >>> vue_news = search_tech_news("Vue.js")
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

@tool(parse_docstring=True)
def search_startup_funding_news(
    max_results: int = 3
) -> Dict[str, Any]:
    """스타트업의 투자 및 채용 관련 최신 뉴스를 검색합니다.
    
    스타트업 투자 유치 소식, 신규 채용 공고, 조직 확장 계획 등을 검색합니다.
    성장하는 스타트업에서 기회를 찾거나 산업 트렌드를 파악하는데 유용합니다.
    
    사용 시점:
    - 투자를 받은 유망 스타트업을 찾을 때
    - 빠르게 성장하는 회사의 채용 기회를 발견할 때
    - 스타트업 생태계의 전반적인 동향을 파악할 때
    - 새로운 비즈니스 모델이나 기술을 가진 회사를 알아볼 때
    
    Args:
        max_results: 반환할 최대 뉴스 수 (기본값: 3, 권장 범위: 3-7)
    
    Returns:
        스타트업 뉴스 검색 결과 딕셔너리:
            - success (bool): 검색 성공 여부
            - count (int): 찾은 뉴스 수
            - startup_news (List[Dict]): 뉴스 리스트. 각 뉴스는 다음 포함:
                - title (str): 뉴스 제목
                - content (str): 뉴스 내용 요약 (투자 규모, 채용 계획 등)
                - url (str): 원본 뉴스 URL
                - score (float): 검색 쿼리와의 관련성 점수
                - published_date (str): 발행일 (가능한 경우)
            - message (str): 검색 결과 요약 메시지
    
    Raises:
        Exception: 스타트업 뉴스 검색 실패 시. 오류는 반환 딕셔너리의 
            'error' 키에 포함됩니다.
    
    Examples:
        >>> news = search_startup_funding_news()
        >>> for article in news['startup_news']:
        ...     print(f"{article['title']}")
        ...     print(f"내용: {article['content'][:150]}...")
        ...     print(f"날짜: {article['published_date']}\n")
        
        >>> # 더 많은 뉴스 수집
        >>> news = search_startup_funding_news(max_results=7)
        >>> investment_news = [n for n in news['startup_news'] 
        ...                    if '투자' in n['title'] or '펀딩' in n['title']]
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