"""정형 데이터 기반 인재 검색 도구들 (PostgreSQL)"""

from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from ..database.repositories import get_candidate_repository

# 저장소 인스턴스
candidate_repo = get_candidate_repository()

@tool
def search_candidates_by_skills(skills: List[str], min_experience: int = 0, proficiency_level: str = None) -> List[Dict[str, Any]]:
    """
    스킬 기반 인재 검색 도구

    Args:
        skills: 검색할 기술 스킬 리스트 (예: ["Python", "React", "AWS"])
        min_experience: 최소 경력 년수 (기본값: 0)
        proficiency_level: 숙련도 수준 ("beginner", "intermediate", "advanced", "expert")

    Returns:
        조건에 맞는 인재 리스트
    """
    try:
        candidates = candidate_repo.search_by_skills(
            skills=skills,
            min_experience=min_experience,
            proficiency=proficiency_level
        )

        return {
            "success": True,
            "count": len(candidates),
            "candidates": candidates[:10],  # 상위 10명만 반환
            "message": f"'{', '.join(skills)}' 스킬을 가진 인재 {len(candidates)}명을 찾았습니다."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "인재 검색 중 오류가 발생했습니다."
        }

@tool
def search_candidates_by_location(location: str, exact_match: bool = False) -> List[Dict[str, Any]]:
    """
    지역 기반 인재 검색 도구

    Args:
        location: 검색할 지역 (예: "서울", "강남구", "경기도")
        exact_match: 정확히 일치하는 지역만 검색할지 여부

    Returns:
        해당 지역의 인재 리스트
    """
    try:
        candidates = candidate_repo.search_by_location(
            location=location,
            exact_match=exact_match
        )

        return {
            "success": True,
            "count": len(candidates),
            "candidates": candidates[:10],
            "message": f"'{location}' 지역의 인재 {len(candidates)}명을 찾았습니다."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "지역 기반 검색 중 오류가 발생했습니다."
        }

@tool
def search_candidates_by_salary_range(min_salary: int, max_salary: int) -> List[Dict[str, Any]]:
    """
    희망 급여 범위 기반 인재 검색 도구

    Args:
        min_salary: 최소 연봉 (만원 단위, 예: 7000)
        max_salary: 최대 연봉 (만원 단위, 예: 10000)

    Returns:
        급여 범위에 맞는 인재 리스트
    """
    try:
        candidates = candidate_repo.search_by_salary_range(
            min_salary=min_salary,
            max_salary=max_salary
        )

        return {
            "success": True,
            "count": len(candidates),
            "candidates": candidates[:10],
            "message": f"연봉 {min_salary}-{max_salary}만원 범위의 인재 {len(candidates)}명을 찾았습니다."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "급여 범위 검색 중 오류가 발생했습니다."
        }

@tool
def search_candidates_by_work_type(work_type: str) -> List[Dict[str, Any]]:
    """
    근무 형태 기반 인재 검색 도구

    Args:
        work_type: 희망 근무 형태 ("remote", "hybrid", "onsite")

    Returns:
        해당 근무 형태를 선호하는 인재 리스트
    """
    try:
        candidates = candidate_repo.search_by_work_type(work_type=work_type)

        work_type_korean = {
            "remote": "원격근무",
            "hybrid": "하이브리드",
            "onsite": "출근"
        }.get(work_type, work_type)

        return {
            "success": True,
            "count": len(candidates),
            "candidates": candidates[:10],
            "message": f"{work_type_korean}를 선호하는 인재 {len(candidates)}명을 찾았습니다."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "근무 형태 검색 중 오류가 발생했습니다."
        }

@tool
def search_candidates_by_industry(industry: str) -> List[Dict[str, Any]]:
    """
    희망 산업 분야 기반 인재 검색 도구

    Args:
        industry: 산업 분야 (예: "Technology", "Fintech", "E-commerce")

    Returns:
        해당 산업을 희망하는 인재 리스트
    """
    try:
        candidates = candidate_repo.search_by_industry(industry=industry)

        return {
            "success": True,
            "count": len(candidates),
            "candidates": candidates[:10],
            "message": f"'{industry}' 산업을 희망하는 인재 {len(candidates)}명을 찾았습니다."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "산업 분야 검색 중 오류가 발생했습니다."
        }

@tool
def search_candidates_by_availability(availability_status: str) -> List[Dict[str, Any]]:
    """
    구직 활동 상태 기반 인재 검색 도구

    Args:
        availability_status: 구직 상태 ("actively_looking", "passively_looking", "not_looking")

    Returns:
        해당 구직 상태의 인재 리스트
    """
    try:
        candidates = candidate_repo.search_by_availability(status=availability_status)

        status_korean = {
            "actively_looking": "적극적으로 구직중",
            "passively_looking": "소극적으로 구직중",
            "not_looking": "구직하지 않음"
        }.get(availability_status, availability_status)

        return {
            "success": True,
            "count": len(candidates),
            "candidates": candidates[:10],
            "message": f"{status_korean}인 인재 {len(candidates)}명을 찾았습니다."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "구직 상태 검색 중 오류가 발생했습니다."
        }

@tool
def get_candidate_details(candidate_id: int) -> Dict[str, Any]:
    """
    특정 인재의 상세 정보 조회 도구

    Args:
        candidate_id: 인재 ID

    Returns:
        인재의 상세 정보
    """
    try:
        candidate = candidate_repo.get_candidate_by_id(candidate_id)

        if not candidate:
            return {
                "success": False,
                "message": f"ID {candidate_id}인 인재를 찾을 수 없습니다."
            }

        return {
            "success": True,
            "candidate": candidate,
            "message": f"{candidate['name']}님의 상세 정보입니다."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "인재 상세 정보 조회 중 오류가 발생했습니다."
        }

@tool
def complex_candidate_search(
    skills: List[str] = None,
    location: str = None,
    min_salary: int = None,
    max_salary: int = None,
    work_type: str = None,
    industry: str = None,
    availability: str = None,
    min_age: int = None,
    max_age: int = None
) -> List[Dict[str, Any]]:
    """
    복합 조건 인재 검색 도구

    Args:
        skills: 기술 스킬 리스트
        location: 지역
        min_salary: 최소 연봉
        max_salary: 최대 연봉
        work_type: 근무 형태
        industry: 산업 분야
        availability: 구직 상태
        min_age: 최소 나이
        max_age: 최대 나이

    Returns:
        모든 조건을 만족하는 인재 리스트
    """
    try:
        filters = {}
        if skills:
            filters['skills'] = skills
        if location:
            filters['location'] = location
        if min_salary:
            filters['salary_min'] = min_salary
        if max_salary:
            filters['salary_max'] = max_salary
        if work_type:
            filters['work_type'] = work_type
        if industry:
            filters['industry'] = industry
        if availability:
            filters['availability'] = availability
        if min_age:
            filters['min_age'] = min_age
        if max_age:
            filters['max_age'] = max_age

        candidates = candidate_repo.complex_search(filters)

        # 조건 요약 생성
        conditions = []
        if skills:
            conditions.append(f"스킬: {', '.join(skills)}")
        if location:
            conditions.append(f"지역: {location}")
        if min_salary or max_salary:
            salary_range = f"{min_salary or '0'}-{max_salary or '∞'}만원"
            conditions.append(f"연봉: {salary_range}")
        if work_type:
            conditions.append(f"근무형태: {work_type}")
        if industry:
            conditions.append(f"산업: {industry}")

        condition_text = ", ".join(conditions) if conditions else "모든 조건"

        return {
            "success": True,
            "count": len(candidates),
            "candidates": candidates[:10],
            "filters_applied": filters,
            "message": f"{condition_text}에 맞는 인재 {len(candidates)}명을 찾았습니다."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "복합 검색 중 오류가 발생했습니다."
        }

@tool
def get_candidate_statistics() -> Dict[str, Any]:
    """
    인재 데이터베이스 통계 정보 조회 도구

    Returns:
        전체 인재 수, 지역별 분포, 인기 스킬 등 통계 정보
    """
    try:
        stats = candidate_repo.get_statistics()

        return {
            "success": True,
            "statistics": stats,
            "message": f"총 {stats['total_candidates']}명의 인재가 등록되어 있습니다."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "통계 정보 조회 중 오류가 발생했습니다."
        }