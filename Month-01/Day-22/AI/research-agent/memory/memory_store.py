"""
Memory Store Module
Provides persistent checkpoint storage and state retrieval for StateGraph execution.
Implements time-travel state rollback, thread isolation, and step-by-step history logs.
"""

import os
import json
import uuid
import time
from typing import Dict, List, Any, Optional
from schemas import CheckpointRecord
from config import config


class MemoryStore:
    """
    Persistent Checkpointer & Thread State Store.
    Saves state snapshots to local JSON storage for durability and time-travel replay.
    """

    def __init__(self, storage_dir: Optional[str] = None):
        self.storage_dir = storage_dir or config.checkpoint_dir
        self.in_memory_checkpoints: Dict[str, List[CheckpointRecord]] = {}
        
        if config.enable_memory_persistence:
            os.makedirs(self.storage_dir, exist_ok=True)

    def save_checkpoint(self, thread_id: str, step_index: int, node_name: str, state: Dict[str, Any]) -> str:
        """Saves an immutable snapshot of graph state at a given node transition."""
        checkpoint_id = f"chk_{step_index}_{uuid.uuid4().hex[:6]}"
        
        # Sanitize state snapshot to ensure JSON serializability
        serializable_state = {}
        for k, v in state.items():
            if k in ("current_thought", "final_report") and v is not None and hasattr(v, "model_dump"):
                serializable_state[k] = v.model_dump()
            elif k in ("citations", "session_memory") and isinstance(v, list):
                serializable_state[k] = [item.model_dump() if hasattr(item, "model_dump") else item for item in v]
            elif k == "tool_history" and isinstance(v, list):
                serializable_state[k] = [item.model_dump() if hasattr(item, "model_dump") else item for item in v]
            elif k == "pending_tool_calls" and isinstance(v, list):
                serializable_state[k] = [item.model_dump() if hasattr(item, "model_dump") else item for item in v]
            else:
                serializable_state[k] = v

        record = CheckpointRecord(
            checkpoint_id=checkpoint_id,
            thread_id=thread_id,
            step_index=step_index,
            node_name=node_name,
            timestamp=time.time(),
            state_snapshot=serializable_state
        )

        # In-memory index
        if thread_id not in self.in_memory_checkpoints:
            self.in_memory_checkpoints[thread_id] = []
        self.in_memory_checkpoints[thread_id].append(record)

        # Disk persistence
        if config.enable_memory_persistence:
            thread_path = os.path.join(self.storage_dir, f"{thread_id}.json")
            try:
                records_data = [rec.model_dump() for rec in self.in_memory_checkpoints[thread_id]]
                with open(thread_path, "w", encoding="utf-8") as f:
                    json.dump(records_data, f, indent=2)
            except Exception as e:
                print(f"[WARN] Failed to write checkpoint to disk: {e}")

        return checkpoint_id

    def get_latest_checkpoint(self, thread_id: str) -> Optional[CheckpointRecord]:
        """Retrieves the most recent state checkpoint for a thread."""
        records = self.get_thread_history(thread_id)
        return records[-1] if records else None

    def get_thread_history(self, thread_id: str) -> List[CheckpointRecord]:
        """Loads all checkpoint records for a given thread."""
        if thread_id in self.in_memory_checkpoints and self.in_memory_checkpoints[thread_id]:
            return self.in_memory_checkpoints[thread_id]

        # Attempt to load from disk
        if config.enable_memory_persistence:
            thread_path = os.path.join(self.storage_dir, f"{thread_id}.json")
            if os.path.exists(thread_path):
                try:
                    with open(thread_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    records = [CheckpointRecord(**item) for item in data]
                    self.in_memory_checkpoints[thread_id] = records
                    return records
                except Exception:
                    pass

        return []

    def rollback_to_checkpoint(self, thread_id: str, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        """Time-Travel: Restores state to a specific prior checkpoint and truncates future steps."""
        records = self.get_thread_history(thread_id)
        for idx, rec in enumerate(records):
            if rec.checkpoint_id == checkpoint_id:
                # Truncate forward history to branch from this checkpoint
                self.in_memory_checkpoints[thread_id] = records[: idx + 1]
                if config.enable_memory_persistence:
                    thread_path = os.path.join(self.storage_dir, f"{thread_id}.json")
                    with open(thread_path, "w", encoding="utf-8") as f:
                        json.dump([r.model_dump() for r in self.in_memory_checkpoints[thread_id]], f, indent=2)
                return rec.state_snapshot
        return None

    def list_threads(self) -> List[str]:
        """Lists all known thread IDs."""
        threads = set(self.in_memory_checkpoints.keys())
        if config.enable_memory_persistence and os.path.exists(self.storage_dir):
            for fname in os.listdir(self.storage_dir):
                if fname.endswith(".json"):
                    threads.add(fname[:-5])
        return sorted(list(threads))


# Global Memory Store Instance
global_memory_store = MemoryStore()
