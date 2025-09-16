#!/usr/bin/env python3
"""
Production readiness validation script for Text Extraction and Analysis project
This script validates that the project is ready for main branch deployment.
"""

import sys
import os
import pandas as pd
import importlib.util

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing module imports...")
    
    try:
        from SRC.Data_ingestion import data_ingestion
        from SRC.utils import Col_Structure
        from SRC.Components.Structure import Analysis
        print("  ✅ All core modules imported successfully")
        return True
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False

def test_dependencies():
    """Test that all required dependencies are available"""
    print("🔍 Testing dependencies...")
    
    required_packages = ['pandas', 'numpy', 'nltk', 'flask', 'bs4', 'openpyxl']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'bs4':
                import bs4
            else:
                __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {missing_packages}")
        return False
    else:
        print("  ✅ All dependencies available")
        return True

def test_file_structure():
    """Test that essential files and directories exist"""
    print("🔍 Testing file structure...")
    
    essential_files = [
        'requirements.txt',
        'setup.py',
        'README.md',
        'SRC/Data_ingestion.py',
        'SRC/utils.py',
        'SRC/Components/Structure.py',
        'SRC/Pipeline/Training_pipeline.py',
        'Notebook/data/Input.xlsx'
    ]
    
    missing_files = []
    for file_path in essential_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"Missing essential files: {missing_files}")
        return False
    else:
        print("  ✅ All essential files present")
        return True

def test_path_portability():
    """Test that the code uses portable paths"""
    print("🔍 Testing path portability...")
    
    # Check for hard-coded Windows paths in Python files
    python_files = [
        'SRC/Data_ingestion.py',
        'SRC/utils.py',
        'SRC/Components/Structure.py'
    ]
    
    issues_found = False
    for file_path in python_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Check for Windows-style paths
                if ':\\' in content or 'E:\\' in content:
                    print(f"  ❌ Hard-coded Windows path found in {file_path}")
                    issues_found = True
                else:
                    print(f"  ✅ {file_path} uses portable paths")
    
    if issues_found:
        return False
    else:
        print("  ✅ All paths are portable")
        return True

def test_functionality():
    """Test core functionality with sample data"""
    print("🔍 Testing core functionality...")
    
    try:
        # Test data ingestion
        from SRC.Data_ingestion import data_ingestion
        obj = data_ingestion()
        data = obj.primary()
        
        if data is not None and len(data) > 0:
            print(f"  ✅ Data ingestion works ({len(data)} records)")
        else:
            print("  ❌ Data ingestion failed")
            return False
        
        # Test analysis with sample data
        from SRC.utils import Col_Structure
        str_obj = Col_Structure()
        
        sample_data = pd.DataFrame({
            'URL_ID': ['test001'],
            'URL': ['https://example.com/test'],
            'article_words': ['This is a positive test article with excellent content and amazing results.']
        })
        
        result = str_obj.Col_Structure_Primary(sample_data)
        if result is not None and len(result) > 0:
            print(f"  ✅ Text analysis works (output shape: {result.shape})")
        else:
            print("  ❌ Text analysis failed")
            return False
        
        print("  ✅ Core functionality validated")
        return True
        
    except Exception as e:
        print(f"  ❌ Functionality test failed: {e}")
        return False

def main():
    """Run all production readiness tests"""
    print("🚀 Text Extraction and Analysis - Production Readiness Validation")
    print("=" * 70)
    
    tests = [
        ("Module Imports", test_imports),
        ("Dependencies", test_dependencies),
        ("File Structure", test_file_structure),
        ("Path Portability", test_path_portability),
        ("Core Functionality", test_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        print()
    
    print("=" * 70)
    print(f"📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ✅ PROJECT IS READY FOR MAIN BRANCH DEPLOYMENT!")
        print("\nThe Text Extraction and Analysis project has been successfully")
        print("prepared for production use with:")
        print("• Portable file paths")
        print("• Robust error handling")
        print("• All dependencies included")
        print("• Validated functionality")
        return True
    else:
        print("❌ Project needs additional fixes before main branch deployment")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)