-- 헤드헌터 AI 에이전트 데이터베이스 초기화 스크립트
-- 정형 데이터만 저장 (임베딩 없음)

-- 인재 기본 정보
CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    age INTEGER,
    location VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active', -- active, inactive, hired
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 경력 정보
CREATE TABLE experiences (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id) ON DELETE CASCADE,
    company_name VARCHAR(200),
    position VARCHAR(200),
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN DEFAULT FALSE,
    description TEXT,
    industry VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 기술 스킬
CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id) ON DELETE CASCADE,
    skill_name VARCHAR(100),
    proficiency_level VARCHAR(20), -- beginner, intermediate, advanced, expert
    years_of_experience DECIMAL(3,1),
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 교육 배경
CREATE TABLE education (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id) ON DELETE CASCADE,
    institution VARCHAR(200),
    degree VARCHAR(100),
    major VARCHAR(100),
    graduation_date DATE,
    gpa DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 급여 및 희망 조건
CREATE TABLE preferences (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id) ON DELETE CASCADE,
    desired_salary_min INTEGER,
    desired_salary_max INTEGER,
    work_type VARCHAR(20), -- remote, hybrid, onsite
    company_size VARCHAR(50), -- startup, small, medium, large, enterprise
    industry_preference TEXT[], -- 배열로 여러 산업 저장
    availability_status VARCHAR(30), -- actively_looking, passively_looking, not_looking
    available_from DATE,
    notice_period VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스 생성 (검색 성능 향상)
CREATE INDEX idx_candidates_location ON candidates(location);
CREATE INDEX idx_candidates_status ON candidates(status);
CREATE INDEX idx_skills_name ON skills(skill_name);
CREATE INDEX idx_skills_candidate_id ON skills(candidate_id);
CREATE INDEX idx_experiences_candidate_id ON experiences(candidate_id);
CREATE INDEX idx_experiences_industry ON experiences(industry);
CREATE INDEX idx_preferences_salary ON preferences(desired_salary_min, desired_salary_max);
CREATE INDEX idx_preferences_work_type ON preferences(work_type);

-- 업데이트 트리거 함수
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 업데이트 트리거 설정
CREATE TRIGGER update_candidates_updated_at BEFORE UPDATE ON candidates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();