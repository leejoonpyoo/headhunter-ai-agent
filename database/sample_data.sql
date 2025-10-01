-- 헤드헌터 AI 에이전트 샘플 데이터 삽입
-- 실제적인 한국 개발자 프로필 데이터

-- 인재 기본 정보 삽입
INSERT INTO candidates (name, email, phone, age, location, status) VALUES
('김소프트', 'kim.soft@email.com', '010-1234-5678', 28, '서울특별시 강남구', 'active'),
('박풀스택', 'park.fullstack@email.com', '010-2345-6789', 32, '서울특별시 서초구', 'active'),
('이데이터', 'lee.data@email.com', '010-3456-7890', 29, '경기도 성남시', 'active'),
('최클라우드', 'choi.cloud@email.com', '010-4567-8901', 35, '서울특별시 종로구', 'active'),
('정모바일', 'jung.mobile@email.com', '010-5678-9012', 27, '서울특별시 마포구', 'active'),
('한시큐리티', 'han.security@email.com', '010-6789-0123', 31, '서울특별시 영등포구', 'active'),
('강인공지능', 'kang.ai@email.com', '010-7890-1234', 26, '경기도 분당시', 'active'),
('윤백엔드', 'yoon.backend@email.com', '010-8901-2345', 30, '서울특별시 강서구', 'active'),
('조프론트', 'cho.frontend@email.com', '010-9012-3456', 25, '서울특별시 송파구', 'active'),
('임게임', 'lim.game@email.com', '010-0123-4567', 33, '경기도 고양시', 'active');

-- 경력 정보 삽입
INSERT INTO experiences (candidate_id, company_name, position, start_date, end_date, is_current, description, industry) VALUES
-- 김소프트 (Python 개발자)
(1, '네이버', 'Senior Python Developer', '2022-03-01', NULL, true, 'Python 기반 웹 서비스 개발 및 API 설계. Django, FastAPI 활용한 백엔드 시스템 구축', 'Technology'),
(1, '카카오', 'Python Developer', '2020-01-15', '2022-02-28', false, 'Python 백엔드 개발, 데이터 파이프라인 구축', 'Technology'),

-- 박풀스택 (풀스택 개발자)
(2, '쿠팡', 'Full Stack Developer', '2021-06-01', NULL, true, 'React + Node.js 기반 이커머스 플랫폼 개발. AWS 인프라 구축 및 운영', 'E-commerce'),
(2, '배달의민족', 'Frontend Developer', '2019-03-01', '2021-05-31', false, 'React, Vue.js를 활용한 프론트엔드 개발', 'Technology'),

-- 이데이터 (데이터 사이언티스트)
(3, 'LG AI Research', 'Data Scientist', '2022-01-01', NULL, true, 'Python, R을 활용한 데이터 분석 및 머신러닝 모델 개발. TensorFlow, PyTorch 활용', 'AI/ML'),
(3, '삼성전자', 'Data Analyst', '2020-06-01', '2021-12-31', false, '데이터 분석, 통계 모델링, 비즈니스 인사이트 도출', 'Electronics'),

-- 최클라우드 (클라우드 엔지니어)
(4, 'AWS Korea', 'Cloud Solutions Architect', '2021-09-01', NULL, true, 'AWS 기반 클라우드 솔루션 설계 및 구축. Kubernetes, Terraform 활용', 'Cloud'),
(4, 'SK텔레콤', 'DevOps Engineer', '2018-07-01', '2021-08-31', false, 'CI/CD 파이프라인 구축, 인프라 자동화', 'Telecommunications'),

-- 정모바일 (모바일 개발자)
(5, '토스', 'Senior Android Developer', '2022-05-01', NULL, true, 'Kotlin 기반 안드로이드 앱 개발. 금융 서비스 앱 아키텍처 설계', 'Fintech'),
(5, '라인', 'Android Developer', '2020-02-01', '2022-04-30', false, 'Java, Kotlin 안드로이드 앱 개발', 'Technology'),

-- 한시큐리티 (보안 전문가)
(6, 'NSHC', 'Security Engineer', '2021-03-01', NULL, true, '웹 애플리케이션 보안, 침투테스트, 보안 컨설팅', 'Security'),
(6, '안랩', 'Security Analyst', '2019-01-01', '2021-02-28', false, '악성코드 분석, 보안 솔루션 개발', 'Security'),

-- 강인공지능 (AI 엔지니어)
(7, '업스테이지', 'AI Engineer', '2023-01-01', NULL, true, 'LLM 모델 개발 및 최적화. Transformer, BERT 모델 연구', 'AI/ML'),
(7, '테스트웍스', 'ML Engineer', '2021-07-01', '2022-12-31', false, '머신러닝 모델 개발 및 배포', 'AI/ML'),

-- 윤백엔드 (백엔드 개발자)
(8, '당근마켓', 'Senior Backend Developer', '2021-04-01', NULL, true, 'Go, Python 기반 백엔드 API 개발. 마이크로서비스 아키텍처 구축', 'Technology'),
(8, '야놀자', 'Backend Developer', '2019-06-01', '2021-03-31', false, 'Java Spring 기반 백엔드 개발', 'Travel'),

-- 조프론트 (프론트엔드 개발자)
(9, '버킷플레이스', 'Frontend Developer', '2022-08-01', NULL, true, 'React, TypeScript 기반 웹 애플리케이션 개발. Next.js 활용', 'Technology'),
(9, '스타일쉐어', 'Junior Frontend Developer', '2021-03-01', '2022-07-31', false, 'Vue.js, JavaScript 프론트엔드 개발', 'Fashion'),

-- 임게임 (게임 개발자)
(10, '넥슨', 'Game Developer', '2020-01-01', NULL, true, 'Unity 3D, C# 기반 모바일 게임 개발. 서버 프로그래밍', 'Gaming'),
(10, '컴투스', 'Game Programmer', '2017-05-01', '2019-12-31', false, 'Unity, C++ 게임 엔진 개발', 'Gaming');

-- 기술 스킬 삽입
INSERT INTO skills (candidate_id, skill_name, proficiency_level, years_of_experience, is_primary) VALUES
-- 김소프트 스킬
(1, 'Python', 'expert', 5.0, true),
(1, 'Django', 'expert', 4.0, true),
(1, 'FastAPI', 'advanced', 2.0, false),
(1, 'PostgreSQL', 'advanced', 3.0, false),
(1, 'AWS', 'intermediate', 2.0, false),

-- 박풀스택 스킬
(2, 'JavaScript', 'expert', 6.0, true),
(2, 'React', 'expert', 5.0, true),
(2, 'Node.js', 'expert', 4.0, true),
(2, 'TypeScript', 'advanced', 3.0, false),
(2, 'AWS', 'advanced', 3.0, false),

-- 이데이터 스킬
(3, 'Python', 'expert', 4.0, true),
(3, 'R', 'advanced', 3.0, false),
(3, 'Machine Learning', 'expert', 3.0, true),
(3, 'TensorFlow', 'advanced', 2.0, false),
(3, 'SQL', 'expert', 4.0, false),

-- 최클라우드 스킬
(4, 'AWS', 'expert', 6.0, true),
(4, 'Kubernetes', 'expert', 4.0, true),
(4, 'Terraform', 'advanced', 3.0, false),
(4, 'Docker', 'expert', 5.0, false),
(4, 'Python', 'intermediate', 3.0, false),

-- 정모바일 스킬
(5, 'Kotlin', 'expert', 4.0, true),
(5, 'Android', 'expert', 5.0, true),
(5, 'Java', 'advanced', 4.0, false),
(5, 'Firebase', 'advanced', 2.0, false),
(5, 'REST API', 'advanced', 3.0, false),

-- 한시큐리티 스킬
(6, 'Penetration Testing', 'expert', 5.0, true),
(6, 'Network Security', 'expert', 6.0, true),
(6, 'Python', 'advanced', 4.0, false),
(6, 'Linux', 'expert', 7.0, false),
(6, 'CISSP', 'expert', 3.0, false),

-- 강인공지능 스킬
(7, 'Python', 'expert', 3.0, true),
(7, 'PyTorch', 'expert', 2.0, true),
(7, 'Transformer', 'expert', 1.5, true),
(7, 'LangChain', 'advanced', 1.0, false),
(7, 'MLflow', 'intermediate', 1.0, false),

-- 윤백엔드 스킬
(8, 'Go', 'expert', 3.0, true),
(8, 'Python', 'advanced', 4.0, false),
(8, 'PostgreSQL', 'expert', 5.0, false),
(8, 'Redis', 'advanced', 3.0, false),
(8, 'Microservices', 'advanced', 2.0, false),

-- 조프론트 스킬
(9, 'React', 'expert', 2.0, true),
(9, 'TypeScript', 'expert', 2.0, true),
(9, 'Next.js', 'advanced', 1.0, false),
(9, 'CSS', 'expert', 3.0, false),
(9, 'JavaScript', 'expert', 3.0, false),

-- 임게임 스킬
(10, 'Unity', 'expert', 7.0, true),
(10, 'C#', 'expert', 8.0, true),
(10, 'C++', 'advanced', 5.0, false),
(10, '3D Graphics', 'advanced', 4.0, false),
(10, 'Game Design', 'expert', 6.0, false);

-- 교육 배경 삽입
INSERT INTO education (candidate_id, institution, degree, major, graduation_date, gpa) VALUES
(1, '서울대학교', '학사', '컴퓨터공학과', '2019-02-28', 3.8),
(2, '연세대학교', '학사', '컴퓨터과학과', '2017-02-28', 3.6),
(3, 'KAIST', '석사', '데이터사이언스', '2020-02-28', 4.0),
(3, '고려대학교', '학사', '통계학과', '2018-02-28', 3.9),
(4, '한양대학교', '학사', '전자공학과', '2016-02-28', 3.7),
(5, '성균관대학교', '학사', '소프트웨어학과', '2020-02-28', 3.5),
(6, '부산대학교', '학사', '정보보호학과', '2017-02-28', 3.8),
(7, 'POSTECH', '석사', '인공지능학과', '2022-02-28', 4.2),
(7, '서울대학교', '학사', '수학과', '2020-02-28', 3.9),
(8, '중앙대학교', '학사', '컴퓨터공학과', '2018-02-28', 3.4),
(9, '이화여자대학교', '학사', '컴퓨터공학과', '2021-02-28', 3.7),
(10, '홍익대학교', '학사', '게임학부', '2016-02-28', 3.6);

-- 희망 조건 삽입
INSERT INTO preferences (candidate_id, desired_salary_min, desired_salary_max, work_type, company_size, industry_preference, availability_status, available_from, notice_period) VALUES
(1, 7000, 9000, 'hybrid', 'medium', ARRAY['Technology', 'Fintech'], 'passively_looking', '2024-04-01', '1개월'),
(2, 8000, 11000, 'remote', 'large', ARRAY['Technology', 'E-commerce'], 'actively_looking', '2024-03-15', '2주'),
(3, 7500, 10000, 'hybrid', 'startup', ARRAY['AI/ML', 'Technology'], 'actively_looking', '2024-03-01', '1개월'),
(4, 9000, 12000, 'onsite', 'enterprise', ARRAY['Cloud', 'Technology'], 'passively_looking', '2024-05-01', '1개월'),
(5, 6500, 8500, 'hybrid', 'medium', ARRAY['Fintech', 'Technology'], 'not_looking', '2024-12-01', '2개월'),
(6, 8500, 11000, 'remote', 'large', ARRAY['Security', 'Technology'], 'actively_looking', '2024-03-01', '1개월'),
(7, 7000, 9500, 'hybrid', 'startup', ARRAY['AI/ML', 'Technology'], 'actively_looking', '2024-02-15', '2주'),
(8, 7500, 9500, 'remote', 'medium', ARRAY['Technology', 'E-commerce'], 'passively_looking', '2024-06-01', '1개월'),
(9, 5500, 7500, 'hybrid', 'startup', ARRAY['Technology', 'Fashion'], 'actively_looking', '2024-03-01', '2주'),
(10, 8000, 10000, 'onsite', 'large', ARRAY['Gaming', 'Technology'], 'passively_looking', '2024-07-01', '1개월');