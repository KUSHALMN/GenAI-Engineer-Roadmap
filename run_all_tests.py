"""
Unified Test Runner for GenAI Engineer Roadmap.
Discovers and executes daily AI and DSA test suites across all months.
"""

import os
import subprocess
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent

TEST_SUITES = [
    {
        "name": "Month-01 Day-17: PDF RAG Chatbot Unit Tests",
        "cwd": ROOT_DIR / "Month-01" / "Day-17" / "AI" / "pdf-rag-chatbot",
        "cmd": [sys.executable, "-m", "unittest", "discover", "tests"],
    },
    {
        "name": "Month-01 Day-19: Tool-Calling Assistant Calculator Tests",
        "cwd": ROOT_DIR / "Month-01" / "Day-19" / "AI" / "tool-calling-assistant",
        "cmd": [sys.executable, "tests/test_calculator.py"],
    },
    {
        "name": "Month-01 Day-22: PDF RAG Chatbot Integration Tests",
        "cwd": ROOT_DIR / "Month-01" / "Day-22" / "AI" / "pdf-rag-chatbot",
        "cmd": [sys.executable, "tests/test_api.py"],
    },
    {
        "name": "Month-01 Day-22: PDF RAG Pipeline Tests",
        "cwd": ROOT_DIR / "Month-01" / "Day-22" / "AI" / "pdf-rag-chatbot",
        "cmd": [sys.executable, "tests/test_rag.py"],
    },
]


def run_tests() -> int:
    print("=" * 70)
    print("🚀 GenAI Engineer Roadmap — Automated Verification Suite")
    print("=" * 70)

    total = len(TEST_SUITES)
    passed = 0
    failed = 0

    for suite in TEST_SUITES:
        name = suite["name"]
        cwd = suite["cwd"]
        cmd = suite["cmd"]

        print(f"\n▶ Running: {name}")
        if not cwd.exists():
            print(f"  ⚠️ Skipped: Directory not found ({cwd})")
            continue

        try:
            res = subprocess.run(
                cmd,
                cwd=str(cwd),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            if res.returncode == 0:
                print(f"  ✅ PASSED")
                passed += 1
            else:
                print(f"  ❌ FAILED (Exit Code {res.returncode})")
                print(res.stdout)
                print(res.stderr)
                failed += 1
        except Exception as e:
            print(f"  ❌ EXCEPTION: {e}")
            failed += 1

    print("\n" + "=" * 70)
    print(f"📊 Summary: {passed}/{total} Passed | {failed} Failed")
    print("=" * 70)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_tests())
