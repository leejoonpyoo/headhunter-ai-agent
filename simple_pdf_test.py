#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple PDF parsing test
"""

import sys
import os

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Import 테스트"""
    try:
        from src.ui.pdf_parser import parse_pdf_jd
        print("PDF parser import: OK")
        
        from src.services.company_extractor import CompanyExtractor
        print("Company extractor import: OK")
        
        return True
    except Exception as e:
        print(f"Import error: {e}")
        return False

def test_pdf_parsing():
    """PDF 파싱 기본 테스트"""
    try:
        from src.ui.pdf_parser import parse_pdf_jd
        import io
        
        # 빈 모의 파일로 테스트
        class MockFile:
            def __init__(self):
                self.content = b""
            
            def read(self):
                return self.content
            
            def seek(self, pos):
                pass
        
        mock_file = MockFile()
        result = parse_pdf_jd(mock_file)
        
        print(f"PDF parsing result: {result}")
        return True
        
    except Exception as e:
        print(f"PDF parsing error: {e}")
        return False

if __name__ == "__main__":
    print("Testing PDF functionality...")
    
    if test_imports():
        print("All imports successful")
        
        if test_pdf_parsing():
            print("PDF parsing test: PASSED")
        else:
            print("PDF parsing test: FAILED")
    else:
        print("Import test: FAILED")
