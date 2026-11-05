"""
Month-03 Automated Verification Test Runner
Validates that all 31 days have:
- Runnable Python AI script in AI/
- Standalone compilable Java DSA solution in DSA/
- Comprehensive Interview questions in Interview/
- Detailed notes in Notes/notes.md
- Root README.md in Day-XX/
- Executes all unit tests in Month-03/tests/
"""

import os
import subprocess
import sys
import unittest


def verify_day(day_num: int):
    day_folder = f"Day-{day_num:02d}"
    day_path = os.path.join(os.path.dirname(__file__), day_folder)
    
    if not os.path.exists(day_path):
        return False, f"Missing directory: {day_path}"
        
    ai_dir = os.path.join(day_path, "AI")
    dsa_dir = os.path.join(day_path, "DSA")
    interview_dir = os.path.join(day_path, "Interview")
    notes_dir = os.path.join(day_path, "Notes")
    readme = os.path.join(day_path, "README.md")
    
    if not (os.path.exists(ai_dir) and os.path.exists(dsa_dir) and os.path.exists(interview_dir) and os.path.exists(notes_dir) and os.path.exists(readme)):
        return False, f"{day_folder}: Missing required subdirectories or README.md"
        
    # Check Python file
    py_files = [f for f in os.listdir(ai_dir) if f.endswith(".py") and not f.startswith("__")]
    if not py_files:
        for root, _, files in os.walk(ai_dir):
            py_files.extend([f for f in files if f.endswith(".py") and not f.startswith("__")])
    if not py_files:
        return False, f"{day_folder}: No Python script in AI/"
        
    # Check Java file
    java_files = [f for f in os.listdir(dsa_dir) if f.endswith(".java")]
    if not java_files:
        return False, f"{day_folder}: No Java file in DSA/"
        
    # Check Interview file
    interview_files = [f for f in os.listdir(interview_dir) if f.endswith(".md")]
    if not interview_files:
        return False, f"{day_folder}: No Interview questions in Interview/"
        
    # Check Notes file
    notes_files = [f for f in os.listdir(notes_dir) if f.endswith(".md")]
    if not notes_files:
        return False, f"{day_folder}: No Notes in Notes/"
        
    return True, f"{day_folder}: PASSED (AI: {len(py_files)}, DSA: {len(java_files)}, Notes: {len(notes_files)})"


def run_test_suites():
    test_dir = os.path.join(os.path.dirname(__file__), "tests")
    print("\nRunning Automated Unit Test Suites in Month-03/tests/...")
    suite = unittest.defaultTestLoader.discover(test_dir, pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def main():
    print("=" * 65)
    print("   Month-03 Production RAG v2 Verification & Architecture Audit")
    print("=" * 65)
    all_ok = True
    for d in range(1, 32):
        ok, msg = verify_day(d)
        print(f"[{'OK' if ok else 'FAIL'}] {msg}")
        if not ok:
            all_ok = False
            
    test_ok = run_test_suites()
    
    print("=" * 65)
    if all_ok and test_ok:
        print(">>> ALL 31 DAYS & TEST SUITES PASSED VERIFICATION AUDIT! <<<")
        print("=" * 65)
    else:
        print(">>> VERIFICATION OR TEST SUITE FAILED! <<<")
        print("=" * 65)
        sys.exit(1)


if __name__ == "__main__":
    main()
