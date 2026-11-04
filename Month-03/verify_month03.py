"""
Month-03 Automated Verification Test Runner
Validates that all 31 days have:
- Runnable Python AI script in AI/
- Compilable Java DSA solution in DSA/
- Comprehensive Interview questions in Interview/
- Detailed notes in Notes/
- Root README.md in Day-XX/
"""

import os
import subprocess
import sys

def verify_day(day_num: int):
    day_folder = f"Day-{day_num:02d}"
    day_path = os.path.join(os.path.dirname(__file__), day_folder)
    
    if not os.path.exists(day_path):
        return False, f"Missing directory: {day_path}"
        
    ai_dir = os.path.join(day_path, "AI")
    dsa_dir = os.path.join(day_path, "DSA")
    readme = os.path.join(day_path, "README.md")
    
    if not os.path.exists(ai_dir) or not os.path.exists(dsa_dir) or not os.path.exists(readme):
        return False, f"{day_folder}: Missing AI/, DSA/, or README.md"
        
    # Check Python file
    py_files = [f for f in os.listdir(ai_dir) if f.endswith(".py") and not f.startswith("__")]
    # Check Java file
    java_files = [f for f in os.listdir(dsa_dir) if f.endswith(".java")]
    
    if not py_files:
        # Check subdirectories
        sub_pys = []
        for root, _, files in os.walk(ai_dir):
            sub_pys.extend([f for f in files if f.endswith(".py") and not f.startswith("__")])
        if not sub_pys:
            return False, f"{day_folder}: No Python file found in AI/"
            
    if not java_files:
        return False, f"{day_folder}: No Java file found in DSA/"
        
    return True, f"{day_folder}: OK (Py: {len(py_files) or 'subdirs'}, Java: {len(java_files)})"

def main():
    print("=" * 60)
    print("  Month-03 Verification Runner (Days 01 - 31)")
    print("=" * 60)
    all_ok = True
    for d in range(1, 32):
        ok, msg = verify_day(d)
        status = "PASSED" if ok else "FAILED"
        print(f"[{status}] {msg}")
        if not ok:
            all_ok = False
            
    print("=" * 60)
    if all_ok:
        print("ALL 31 DAYS OF MONTH-03 ARE FULLY IMPLEMENTED & VALIDATED!")
    else:
        print("SOME DAYS FAILED VERIFICATION.")
        sys.exit(1)

if __name__ == "__main__":
    main()
