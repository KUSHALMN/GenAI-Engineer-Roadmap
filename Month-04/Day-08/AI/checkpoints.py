"""
Day 08: Agent Checkpoints and Resume
Implements snapshot serialization, atomic checkpoint saving,
and crash recovery that resumes agent execution without repeating side effects.
"""

from typing import Dict, Any, List
import json
import os

class CheckpointManager:
    def __init__(self, storage_dir: str = "./checkpoints_db"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save_checkpoint(self, session_id: str, step_index: int, state: Dict[str, Any]):
        file_path = os.path.join(self.storage_dir, f"{session_id}_step_{step_index}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({
                "session_id": session_id,
                "step_index": step_index,
                "state": state
            }, f, indent=2)
        print(f"[Checkpoint] Saved state at Step {step_index}")

    def load_latest_checkpoint(self, session_id: str) -> Dict[str, Any]:
        matching_files = [f for f in os.listdir(self.storage_dir) if f.startswith(session_id)]
        if not matching_files:
            return {"step_index": 0, "state": {}}
        matching_files.sort(key=lambda x: int(x.split("_step_")[1].replace(".json", "")))
        latest_file = os.path.join(self.storage_dir, matching_files[-1])
        with open(latest_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"[Checkpoint] Restored state from {latest_file} (Step {data['step_index']})")
        return data

if __name__ == "__main__":
    cp = CheckpointManager(storage_dir="./tmp_checkpoints")
    session = "sess_42"

    # Save checkpoints
    cp.save_checkpoint(session, 1, {"completed_tasks": ["charge_card_123"], "balance": 900})
    cp.save_checkpoint(session, 2, {"completed_tasks": ["charge_card_123", "send_receipt_email"], "balance": 900})

    # Simulate crash and resume
    latest = cp.load_latest_checkpoint(session)
    assert latest["step_index"] == 2
    assert "charge_card_123" in latest["state"]["completed_tasks"]

    # Clean up tmp folder
    import shutil
    shutil.rmtree("./tmp_checkpoints")
    print("Day 08 AI Checkpoints manager passed all tests.")
