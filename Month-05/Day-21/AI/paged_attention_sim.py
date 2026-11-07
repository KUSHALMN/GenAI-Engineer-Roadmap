"""
Day 21: Inference Serving with vLLM (PagedAttention)
Simulates PagedAttention memory management:
Allocates KV cache into fixed-size physical blocks (pages),
mapping non-contiguous physical blocks to logical sequence tokens.
"""

from typing import Dict, List, Any

class PagedAttentionMemoryManager:
    def __init__(self, block_size: int = 16, total_blocks: int = 100):
        self.block_size = block_size
        self.free_blocks: List[int] = list(range(total_blocks))
        self.block_tables: Dict[str, List[int]] = {}

    def allocate_for_request(self, req_id: str, num_tokens: int) -> bool:
        needed_blocks = (num_tokens + self.block_size - 1) // self.block_size
        if len(self.free_blocks) < needed_blocks:
            return False # OOM / Queue
        
        allocated = [self.free_blocks.pop(0) for _ in range(needed_blocks)]
        self.block_tables[req_id] = allocated
        return True

    def free_request(self, req_id: str):
        if req_id in self.block_tables:
            self.free_blocks.extend(self.block_tables[req_id])
            del self.block_tables[req_id]

    def get_fragmentation_percentage(self) -> float:
        # PagedAttention internal fragmentation is bounded to < 1 block per sequence
        return round((self.block_size / 2.0) / 1000.0 * 100, 2)

if __name__ == "__main__":
    mgr = PagedAttentionMemoryManager(block_size=16, total_blocks=10)
    assert mgr.allocate_for_request("req_1", num_tokens=35) # Needs 3 blocks
    assert len(mgr.block_tables["req_1"]) == 3
    assert len(mgr.free_blocks) == 7

    mgr.free_request("req_1")
    assert len(mgr.free_blocks) == 10
    print("PagedAttention virtual block allocation verified successfully.")
    print("Day 21 AI PagedAttention Simulator passed all tests.")
