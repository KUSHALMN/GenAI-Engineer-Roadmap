"""
3D Parallelism Orchestrator: Composing Data Parallelism (DP), Tensor Parallelism (TP),
and Pipeline Parallelism (PP) into a Unified 3D Cartesian Grid Topology.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class ParallelismConfig:
    dp_size: int
    tp_size: int
    pp_size: int

    @property
    def world_size(self) -> int:
        return self.dp_size * self.tp_size * self.pp_size


class ClusterTopologyGrid:
    """
    Maps global GPU ranks [0 .. WorldSize - 1] to 3D Cartesian coordinates (dp, pp, tp)
    and determines intra-node NVLink vs inter-node InfiniBand process group placements.
    """
    def __init__(self, config: ParallelismConfig):
        self.config = config
        self.rank_to_coords: Dict[int, Tuple[int, int, int]] = {}
        self.coords_to_rank: Dict[Tuple[int, int, int], int] = {}
        self._build_grid()

    def _build_grid(self):
        # Megatron-LM canonical rank assignment ordering: TP (fastest moving) -> DP -> PP
        for r in range(self.config.world_size):
            tp_rank = r % self.config.tp_size
            dp_rank = (r // self.config.tp_size) % self.config.dp_size
            pp_rank = r // (self.config.tp_size * self.config.dp_size)

            coords = (dp_rank, pp_rank, tp_rank)
            self.rank_to_coords[r] = coords
            self.coords_to_rank[coords] = r

    def get_tp_group(self, rank: int) -> List[int]:
        """Returns all ranks sharing the same DP and PP coordinates as this rank."""
        dp, pp, _ = self.rank_to_coords[rank]
        return [self.coords_to_rank[(dp, pp, tp)] for tp in range(self.config.tp_size)]

    def get_dp_group(self, rank: int) -> List[int]:
        """Returns all ranks sharing the same PP and TP coordinates as this rank."""
        _, pp, tp = self.rank_to_coords[rank]
        return [self.coords_to_rank[(dp, pp, tp)] for dp in range(self.config.dp_size)]

    def get_pp_group(self, rank: int) -> List[int]:
        """Returns all ranks forming the pipeline stages for this rank."""
        dp, _, tp = self.rank_to_coords[rank]
        return [self.coords_to_rank[(dp, pp, tp)] for pp in range(self.config.pp_size)]


if __name__ == "__main__":
    # Cluster configuration: 64 GPUs total (DP=4, PP=2, TP=8)
    # TP=8 fits cleanly inside a single 8-GPU DGX H100 node with NVLink!
    cfg = ParallelismConfig(dp_size=4, tp_size=8, pp_size=2)
    grid = ClusterTopologyGrid(cfg)

    assert cfg.world_size == 64
    rank_0_coords = grid.rank_to_coords[0]
    print(f"Rank 0 3D Coordinates (DP, PP, TP): {rank_0_coords}")
    assert rank_0_coords == (0, 0, 0)

    tp_group_0 = grid.get_tp_group(0)
    print("Rank 0 Tensor Parallel Group (NVLink bound):", tp_group_0)
    assert tp_group_0 == list(range(8)) # GPUs 0-7 form intra-node TP group

    dp_group_0 = grid.get_dp_group(0)
    print("Rank 0 Data Parallel Group (InfiniBand bound):", dp_group_0)
    assert len(dp_group_0) == 4

    print("Day 08 3D Parallelism Orchestrator verification passed.")
