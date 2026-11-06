"""
Day 25: Agent Sandboxing and Side-Effect Control
Implements path allowlisting, dry-run simulation mode,
and rollback logging for modified resources.
"""

from typing import Dict, Any, List
import os

class SandboxedEnvironment:
    def __init__(self, allowed_directory: str, dry_run: bool = False):
        self.allowed_dir = os.path.abspath(allowed_directory)
        self.dry_run = dry_run
        self.rollback_journal: List[Dict[str, Any]] = []

    def safe_write_file(self, relative_path: str, content: str) -> Dict[str, Any]:
        target = os.path.abspath(os.path.join(self.allowed_dir, relative_path))
        if not target.startswith(self.allowed_dir):
            return {"success": False, "error": "Access Denied: Path outside sandbox boundary."}

        if self.dry_run:
            return {"success": True, "dry_run": True, "action": f"Would write {len(content)} bytes to {relative_path}"}

        # Record rollback journal entry
        existed = os.path.exists(target)
        old_content = None
        if existed:
            with open(target, "r", encoding="utf-8") as f:
                old_content = f.read()

        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)

        self.rollback_journal.append({
            "path": target,
            "existed": existed,
            "old_content": old_content
        })
        return {"success": True, "path": target, "dry_run": False}

    def rollback(self):
        """Rollback all modifications recorded in journal."""
        while self.rollback_journal:
            entry = self.rollback_journal.pop()
            if entry["existed"]:
                with open(entry["path"], "w", encoding="utf-8") as f:
                    f.write(entry["old_content"])
            else:
                if os.path.exists(entry["path"]):
                    os.remove(entry["path"])
        print("[Sandbox] Successfully rolled back all side effects.")

if __name__ == "__main__":
    sandbox = SandboxedEnvironment("./tmp_sandbox", dry_run=False)

    # Allowed write
    w1 = sandbox.safe_write_file("data.txt", "Sandbox test file")
    assert w1["success"] is True

    # Path traversal attempt outside sandbox
    w2 = sandbox.safe_write_file("../outside.txt", "Malicious content")
    assert w2["success"] is False
    print(f"Path boundary enforced: {w2['error']}")

    # Rollback test
    sandbox.rollback()
    assert not os.path.exists("./tmp_sandbox/data.txt")

    # Clean up
    import shutil
    if os.path.exists("./tmp_sandbox"):
        shutil.rmtree("./tmp_sandbox")
    print("Day 25 AI Agent Sandbox passed all tests.")
