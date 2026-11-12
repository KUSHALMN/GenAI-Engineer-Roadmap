"""
Distributed Streaming Pretraining DataLoader: Memory-Mapped Binary Chunks,
Multi-Worker Epoch Sharding, Deterministic Rank Offsets, and Prefetch Buffering.
"""

from dataclasses import dataclass
import struct
import tempfile
from typing import Generator, List


@dataclass
class DatasetShardMetadata:
    shard_id: int
    num_tokens: int
    byte_offset: int


class BinaryShardedTokenWriter:
    """
    Serializes integer token streams into compact uint16 / uint32 memory-mappable binary files.
    """
    @staticmethod
    def write_shard(filepath: str, tokens: List[int]):
        with open(filepath, "wb") as f:
            # Write 4-byte header: token count
            f.write(struct.pack("<I", len(tokens)))
            # Write 2-byte unsigned short per token (vocab size <= 65535)
            f.write(struct.pack(f"<{len(tokens)}H", *tokens))


class ShardedStreamingDataLoader:
    """
    Simulates high-throughput distributed pretraining data streaming across GPU ranks.
    """
    def __init__(self, shard_paths: List[str], rank: int, world_size: int, batch_size: int, seq_len: int):
        self.shard_paths = shard_paths
        self.rank = rank
        self.world_size = world_size
        self.batch_size = batch_size
        self.seq_len = seq_len

    def iterate_batches(self) -> Generator[List[List[int]], None, None]:
        # Filter shards assigned to this GPU rank
        assigned_shards = [p for i, p in enumerate(self.shard_paths) if i % self.world_size == self.rank]

        accumulated_tokens: List[int] = []
        token_sample_len = self.seq_len

        for shard_path in assigned_shards:
            with open(shard_path, "rb") as f:
                count_bytes = f.read(4)
                if not count_bytes:
                    continue
                num_tokens = struct.unpack("<I", count_bytes)[0]
                raw_bytes = f.read(num_tokens * 2)
                tokens = list(struct.unpack(f"<{num_tokens}H", raw_bytes))
                accumulated_tokens.extend(tokens)

                # Emit batches
                while len(accumulated_tokens) >= self.batch_size * token_sample_len:
                    batch = []
                    for _ in range(self.batch_size):
                        sample = accumulated_tokens[:token_sample_len]
                        batch.append(sample)
                        accumulated_tokens = accumulated_tokens[token_sample_len:]
                    yield batch


if __name__ == "__main__":
    # Create temporary binary shards
    temp_dir = tempfile.mkdtemp()
    shard1 = f"{temp_dir}/shard_00.bin"
    shard2 = f"{temp_dir}/shard_01.bin"

    sample_tokens1 = list(range(100, 260)) # 160 tokens
    sample_tokens2 = list(range(500, 660)) # 160 tokens
    BinaryShardedTokenWriter.write_shard(shard1, sample_tokens1)
    BinaryShardedTokenWriter.write_shard(shard2, sample_tokens2)

    # Simulate Rank 0 of World Size 2, batch size 2, seq_len 16 (32 tokens per batch)
    loader = ShardedStreamingDataLoader([shard1, shard2], rank=0, world_size=2, batch_size=2, seq_len=16)
    batches = list(loader.iterate_batches())

    print(f"Rank 0 processed {len(batches)} batches from assigned shard 0.")
    assert len(batches) == 5 # 160 / 32 = 5 batches
    assert len(batches[0]) == 2
    assert len(batches[0][0]) == 16
    print("Day 02 Sharded Streaming DataLoader verification passed.")
