"""데이터 액세스 레이어 - PostgreSQL 쿼리 인터페이스"""

from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, text, func
from .models import Candidate, Experience, Skill, Education, Preference
from .connection import get_db_session, is_db_available

class CandidateRepository:
    """인재 정보 저장소 클래스"""

    def __init__(self):
        self.db: Optional[Session] = get_db_session()
        self.is_available: bool = is_db_available()

    def get_all_candidates(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """모든 인재 조회"""
        if not self.is_available or not self.db:
            return []

        try:
            candidates = self.db.query(Candidate)\
                .options(
                    joinedload(Candidate.experiences),
                    joinedload(Candidate.skills),
                    joinedload(Candidate.education),
                    joinedload(Candidate.preferences)
                )\
                .filter(Candidate.status == 'active')\
                .limit(limit)\
                .offset(offset)\
                .all()

            return [self._candidate_to_dict(candidate) for candidate in candidates]
        except Exception as e:
            print(f"인재 조회 중 오류: {e}")
            return []

    def get_candidate_by_id(self, candidate_id: int) -> Optional[Dict[str, Any]]:
        """ID로 인재 조회"""
        candidate = self.db.query(Candidate)\
            .options(
                joinedload(Candidate.experiences),
                joinedload(Candidate.skills),
                joinedload(Candidate.education),
                joinedload(Candidate.preferences)
            )\
            .filter(Candidate.id == candidate_id)\
            .first()

        return self._candidate_to_dict(candidate) if candidate else None

    def search_by_skills(self, skills: List[str], min_experience: int = 0, proficiency: str = None) -> List[Dict[str, Any]]:
        """스킬 기반 인재 검색"""
        query = self.db.query(Candidate)\
            .join(Skill)\
            .options(
                joinedload(Candidate.experiences),
                joinedload(Candidate.skills),
                joinedload(Candidate.education),
                joinedload(Candidate.preferences)
            )\
            .filter(Candidate.status == 'active')

        # 스킬 이름 필터
        skill_conditions = [Skill.skill_name.ilike(f'%{skill}%') for skill in skills]
        query = query.filter(or_(*skill_conditions))

        # 경험 년수 필터
        if min_experience > 0:
            query = query.filter(Skill.years_of_experience >= min_experience)

        # 숙련도 필터
        if proficiency:
            query = query.filter(Skill.proficiency_level == proficiency)

        candidates = query.distinct().all()
        return [self._candidate_to_dict(candidate) for candidate in candidates]

    def search_by_location(self, location: str, exact_match: bool = False) -> List[Dict[str, Any]]:
        """지역 기반 인재 검색"""
        query = self.db.query(Candidate)\
            .options(
                joinedload(Candidate.experiences),
                joinedload(Candidate.skills),
                joinedload(Candidate.education),
                joinedload(Candidate.preferences)
            )\
            .filter(Candidate.status == 'active')

        if exact_match:
            query = query.filter(Candidate.location == location)
        else:
            query = query.filter(Candidate.location.ilike(f'%{location}%'))

        candidates = query.all()
        return [self._candidate_to_dict(candidate) for candidate in candidates]

    def search_by_salary_range(self, min_salary: int, max_salary: int) -> List[Dict[str, Any]]:
        """급여 범위 기반 인재 검색"""
        candidates = self.db.query(Candidate)\
            .join(Preference)\
            .options(
                joinedload(Candidate.experiences),
                joinedload(Candidate.skills),
                joinedload(Candidate.education),
                joinedload(Candidate.preferences)
            )\
            .filter(
                Candidate.status == 'active',
                Preference.desired_salary_min <= max_salary,
                Preference.desired_salary_max >= min_salary
            )\
            .all()

        return [self._candidate_to_dict(candidate) for candidate in candidates]

    def search_by_work_type(self, work_type: str) -> List[Dict[str, Any]]:
        """근무 형태 기반 인재 검색"""
        candidates = self.db.query(Candidate)\
            .join(Preference)\
            .options(
                joinedload(Candidate.experiences),
                joinedload(Candidate.skills),
                joinedload(Candidate.education),
                joinedload(Candidate.preferences)
            )\
            .filter(
                Candidate.status == 'active',
                Preference.work_type == work_type
            )\
            .all()

        return [self._candidate_to_dict(candidate) for candidate in candidates]

    def search_by_industry(self, industry: str) -> List[Dict[str, Any]]:
        """희망 산업 기반 인재 검색"""
        candidates = self.db.query(Candidate)\
            .join(Preference)\
            .options(
                joinedload(Candidate.experiences),
                joinedload(Candidate.skills),
                joinedload(Candidate.education),
                joinedload(Candidate.preferences)
            )\
            .filter(
                Candidate.status == 'active',
                Preference.industry_preference.contains([industry])
            )\
            .all()

        return [self._candidate_to_dict(candidate) for candidate in candidates]

    def search_by_availability(self, status: str) -> List[Dict[str, Any]]:
        """구직 상태 기반 인재 검색"""
        candidates = self.db.query(Candidate)\
            .join(Preference)\
            .options(
                joinedload(Candidate.experiences),
                joinedload(Candidate.skills),
                joinedload(Candidate.education),
                joinedload(Candidate.preferences)
            )\
            .filter(
                Candidate.status == 'active',
                Preference.availability_status == status
            )\
            .all()

        return [self._candidate_to_dict(candidate) for candidate in candidates]

    def complex_search(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """복합 조건 검색"""
        query = self.db.query(Candidate)\
            .options(
                joinedload(Candidate.experiences),
                joinedload(Candidate.skills),
                joinedload(Candidate.education),
                joinedload(Candidate.preferences)
            )\
            .filter(Candidate.status == 'active')

        # 기본 정보 필터
        if filters.get('location'):
            query = query.filter(Candidate.location.ilike(f"%{filters['location']}%"))

        if filters.get('min_age') or filters.get('max_age'):
            if filters.get('min_age'):
                query = query.filter(Candidate.age >= filters['min_age'])
            if filters.get('max_age'):
                query = query.filter(Candidate.age <= filters['max_age'])

        # 스킬 필터
        if filters.get('skills'):
            query = query.join(Skill)
            skill_conditions = [Skill.skill_name.ilike(f'%{skill}%') for skill in filters['skills']]
            query = query.filter(or_(*skill_conditions))

        # 희망 조건 필터
        if any(key in filters for key in ['salary_min', 'salary_max', 'work_type', 'industry', 'availability']):
            query = query.join(Preference)

            if filters.get('salary_min') or filters.get('salary_max'):
                if filters.get('salary_min'):
                    query = query.filter(Preference.desired_salary_max >= filters['salary_min'])
                if filters.get('salary_max'):
                    query = query.filter(Preference.desired_salary_min <= filters['salary_max'])

            if filters.get('work_type'):
                query = query.filter(Preference.work_type == filters['work_type'])

            if filters.get('industry'):
                query = query.filter(Preference.industry_preference.contains([filters['industry']]))

            if filters.get('availability'):
                query = query.filter(Preference.availability_status == filters['availability'])

        candidates = query.distinct().all()
        return [self._candidate_to_dict(candidate) for candidate in candidates]

    def get_statistics(self) -> Dict[str, Any]:
        """인재 통계 정보"""
        if not self.is_available or not self.db:
            return {
                'total_candidates': 0,
                'location_distribution': [],
                'top_skills': [],
                'work_type_distribution': [],
                'error': 'Database not available'
            }

        try:
            total_candidates = self.db.query(Candidate).filter(Candidate.status == 'active').count()

            # 지역별 통계
            location_stats = self.db.query(
                Candidate.location,
                func.count(Candidate.id).label('count')
            ).filter(Candidate.status == 'active')\
             .group_by(Candidate.location)\
             .all()

            # 스킬별 통계
            skill_stats = self.db.query(
                Skill.skill_name,
                func.count(Skill.id).label('count')
            ).join(Candidate)\
             .filter(Candidate.status == 'active')\
             .group_by(Skill.skill_name)\
             .order_by(func.count(Skill.id).desc())\
             .limit(10)\
             .all()

            # 근무 형태별 통계
            work_type_stats = self.db.query(
                Preference.work_type,
                func.count(Preference.id).label('count')
            ).join(Candidate)\
             .filter(Candidate.status == 'active')\
             .group_by(Preference.work_type)\
             .all()

            return {
                'total_candidates': total_candidates,
                'location_distribution': [{'location': loc, 'count': count} for loc, count in location_stats],
                'top_skills': [{'skill': skill, 'count': count} for skill, count in skill_stats],
                'work_type_distribution': [{'work_type': wt, 'count': count} for wt, count in work_type_stats]
            }
        except Exception as e:
            print(f"통계 조회 중 오류: {e}")
            return {
                'total_candidates': 0,
                'location_distribution': [],
                'top_skills': [],
                'work_type_distribution': [],
                'error': str(e)
            }

    def _candidate_to_dict(self, candidate: Candidate) -> Dict[str, Any]:
        """Candidate 객체를 딕셔너리로 변환"""
        if not candidate:
            return {}

        return {
            **candidate.to_dict(),
            'experiences': [exp.to_dict() for exp in candidate.experiences],
            'skills': [skill.to_dict() for skill in candidate.skills],
            'education': [edu.to_dict() for edu in candidate.education],
            'preferences': [pref.to_dict() for pref in candidate.preferences]
        }

    def close(self):
        """데이터베이스 세션 종료"""
        self.db.close()

# 전역 저장소 인스턴스
_repository_instance = None

def get_candidate_repository() -> CandidateRepository:
    """전역 저장소 인스턴스 반환"""
    global _repository_instance
    if _repository_instance is None:
        _repository_instance = CandidateRepository()
    return _repository_instance