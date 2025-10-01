"""프로젝트 초기 설정 스크립트"""

import os
import sys
from pathlib import Path

# 프로젝트 루트 경로
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def create_env_file():
    """환경 변수 파일 생성"""
    env_path = project_root / ".env"
    env_example_path = project_root / ".env.example"

    if not env_path.exists():
        if env_example_path.exists():
            # .env.example을 .env로 복사
            with open(env_example_path, 'r', encoding='utf-8') as f:
                content = f.read()

            with open(env_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print("✅ .env 파일이 생성되었습니다.")
            print("⚠️  .env 파일에서 API 키들을 실제 값으로 변경해주세요.")
        else:
            print("❌ .env.example 파일을 찾을 수 없습니다.")
    else:
        print("✅ .env 파일이 이미 존재합니다.")

def setup_database():
    """데이터베이스 설정"""
    print("\n📊 데이터베이스 설정 중...")

    try:
        # 환경 변수 로드
        from dotenv import load_dotenv
        load_dotenv()

        # 데이터베이스 연결 테스트
        from src.database.connection import get_db_session
        from src.database.models import Base
        from src.database.connection import get_engine

        # 테이블 생성
        engine = get_engine()
        Base.metadata.create_all(bind=engine)

        print("✅ 데이터베이스 테이블이 생성되었습니다.")

        # 샘플 데이터 로드 (선택사항)
        load_sample = input("샘플 인재 데이터를 로드하시겠습니까? (y/n): ").lower().strip()
        if load_sample == 'y':
            load_sample_data()

    except Exception as e:
        print(f"❌ 데이터베이스 설정 중 오류 발생: {e}")
        print("💡 PostgreSQL이 실행 중인지 확인하고, .env 파일의 DB 설정을 확인해주세요.")

def load_sample_data():
    """샘플 데이터 로드"""
    try:
        import subprocess
        import os

        # 환경 변수에서 DB 정보 가져오기
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'headhunter_db')
        db_user = os.getenv('DB_USER', 'headhunter_user')
        db_password = os.getenv('DB_PASSWORD', 'headhunter_pass')

        # PostgreSQL 환경 변수 설정
        env = os.environ.copy()
        env['PGPASSWORD'] = db_password

        # 샘플 데이터 파일 경로
        sample_data_path = project_root / "database" / "sample_data.sql"

        if sample_data_path.exists():
            # psql 명령어로 샘플 데이터 삽입
            cmd = [
                'psql',
                '-h', db_host,
                '-p', db_port,
                '-U', db_user,
                '-d', db_name,
                '-f', str(sample_data_path)
            ]

            result = subprocess.run(cmd, env=env, capture_output=True, text=True)

            if result.returncode == 0:
                print("✅ 샘플 인재 데이터가 성공적으로 로드되었습니다.")
            else:
                print(f"❌ 샘플 데이터 로드 실패: {result.stderr}")
                print("💡 수동으로 database/sample_data.sql 파일을 실행해주세요.")
        else:
            print("❌ 샘플 데이터 파일을 찾을 수 없습니다.")

    except Exception as e:
        print(f"❌ 샘플 데이터 로드 중 오류: {e}")

def setup_vector_store():
    """벡터 스토어 설정"""
    print("\n🔍 벡터 스토어 설정 중...")

    try:
        from src.vector_store.knowledge_loader import initialize_knowledge_base

        # 지식 베이스 초기화
        initialize_knowledge_base()
        print("✅ 벡터 스토어와 지식 베이스가 설정되었습니다.")

    except Exception as e:
        print(f"❌ 벡터 스토어 설정 중 오류 발생: {e}")

def main():
    """메인 설정 함수"""
    print("🚀 헤드헌터 AI 에이전트 프로젝트 초기 설정을 시작합니다...")

    # 1. 환경 변수 파일 생성
    print("\n1️⃣ 환경 변수 파일 설정")
    create_env_file()

    # 2. 데이터베이스 설정
    print("\n2️⃣ 데이터베이스 설정")
    setup_db = input("데이터베이스를 설정하시겠습니까? (PostgreSQL이 실행 중이어야 합니다) (y/n): ").lower().strip()
    if setup_db == 'y':
        setup_database()

    # 3. 벡터 스토어 설정
    print("\n3️⃣ 벡터 스토어 설정")
    setup_vector = input("벡터 스토어와 지식 베이스를 설정하시겠습니까? (y/n): ").lower().strip()
    if setup_vector == 'y':
        setup_vector_store()

    print("\n🎉 설정이 완료되었습니다!")
    print("\n📋 다음 단계:")
    print("1. .env 파일에서 API 키들을 실제 값으로 변경하세요")
    print("2. PostgreSQL이 실행 중인지 확인하세요 (docker-compose up -d)")
    print("3. 패키지를 설치하세요 (pip install -r requirements.txt)")
    print("4. Streamlit 앱을 실행하세요 (python streamlit_run.py)")

if __name__ == "__main__":
    main()