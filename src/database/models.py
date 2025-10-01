"""SQLAlchemy 모델 정의 (정형 데이터만)"""

from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Date, Boolean, Text, DECIMAL, TIMESTAMP, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .connection import Base

class Candidate(Base):
    """인재 기본 정보 모델"""
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20))
    age = Column(Integer)
    location = Column(String(100), index=True)
    status = Column(String(20), default='active', index=True)  # active, inactive, hired
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    # 관계 설정
    experiences = relationship("Experience", back_populates="candidate", cascade="all, delete-orphan")
    skills = relationship("Skill", back_populates="candidate", cascade="all, delete-orphan")
    education = relationship("Education", back_populates="candidate", cascade="all, delete-orphan")
    preferences = relationship("Preference", back_populates="candidate", cascade="all, delete-orphan")

    def to_dict(self):
        """딕셔너리 변환"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'age': self.age,
            'location': self.location,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Experience(Base):
    """경력 정보 모델"""
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    company_name = Column(String(200))
    position = Column(String(200))
    start_date = Column(Date)
    end_date = Column(Date)
    is_current = Column(Boolean, default=False)
    description = Column(Text)
    industry = Column(String(100), index=True)
    created_at = Column(TIMESTAMP, default=func.now())

    # 관계 설정
    candidate = relationship("Candidate", back_populates="experiences")

    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'company_name': self.company_name,
            'position': self.position,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_current': self.is_current,
            'description': self.description,
            'industry': self.industry
        }

class Skill(Base):
    """기술 스킬 모델"""
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    skill_name = Column(String(100), index=True)
    proficiency_level = Column(String(20))  # beginner, intermediate, advanced, expert
    years_of_experience = Column(DECIMAL(3, 1))
    is_primary = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=func.now())

    # 관계 설정
    candidate = relationship("Candidate", back_populates="skills")

    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'skill_name': self.skill_name,
            'proficiency_level': self.proficiency_level,
            'years_of_experience': float(self.years_of_experience) if self.years_of_experience else None,
            'is_primary': self.is_primary
        }

class Education(Base):
    """교육 배경 모델"""
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    institution = Column(String(200))
    degree = Column(String(100))
    major = Column(String(100))
    graduation_date = Column(Date)
    gpa = Column(DECIMAL(3, 2))
    created_at = Column(TIMESTAMP, default=func.now())

    # 관계 설정
    candidate = relationship("Candidate", back_populates="education")

    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'institution': self.institution,
            'degree': self.degree,
            'major': self.major,
            'graduation_date': self.graduation_date.isoformat() if self.graduation_date else None,
            'gpa': float(self.gpa) if self.gpa else None
        }

class Preference(Base):
    """희망 조건 모델"""
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    desired_salary_min = Column(Integer)
    desired_salary_max = Column(Integer)
    work_type = Column(String(20), index=True)  # remote, hybrid, onsite
    company_size = Column(String(50))  # startup, small, medium, large, enterprise
    industry_preference = Column(ARRAY(Text))  # 배열로 여러 산업 저장
    availability_status = Column(String(30))  # actively_looking, passively_looking, not_looking
    available_from = Column(Date)
    notice_period = Column(String(50))
    created_at = Column(TIMESTAMP, default=func.now())

    # 관계 설정
    candidate = relationship("Candidate", back_populates="preferences")

    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'desired_salary_min': self.desired_salary_min,
            'desired_salary_max': self.desired_salary_max,
            'work_type': self.work_type,
            'company_size': self.company_size,
            'industry_preference': self.industry_preference,
            'availability_status': self.availability_status,
            'available_from': self.available_from.isoformat() if self.available_from else None,
            'notice_period': self.notice_period
        }