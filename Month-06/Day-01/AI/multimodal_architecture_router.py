"""
Multimodal Architecture Ingestion Router & Token Budgeting Engine.
Supports text, image, audio, and video inputs with token estimation,
modality-specific validation, and early/late fusion routing.
"""

from dataclasses import dataclass, field
from enum import Enum
import math
import time
from typing import Any, Dict, List, Optional, Tuple


class ModalityType(Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"


class FusionStrategy(Enum):
    EARLY_FUSION = "early_fusion"
    LATE_FUSION = "late_fusion"
    HYBRID = "hybrid"


@dataclass
class ModalityPayload:
    modality: ModalityType
    content: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    estimated_tokens: int = 0


@dataclass
class MultimodalRequest:
    request_id: str
    payloads: List[ModalityPayload]
    target_fusion: FusionStrategy = FusionStrategy.EARLY_FUSION
    total_token_budget: int = 4096
    metadata: Dict[str, Any] = field(default_factory=dict)


class ModalityTokenEstimator:
    PATCH_SIZE = 14
    IMAGE_BASE_TOKENS = 85
    IMAGE_TILE_TOKENS = 170
    AUDIO_TOKENS_PER_SECOND = 12.5
    VIDEO_SAMPLE_FPS = 1.0

    @classmethod
    def estimate_text(cls, text: str) -> int:
        words = len(text.split())
        return max(1, int(words * 1.33))

    @classmethod
    def estimate_image(cls, width: int, height: int, detail: str = "high") -> int:
        if detail == "low":
            return cls.IMAGE_BASE_TOKENS
        tiles_x = math.ceil(width / 512)
        tiles_y = math.ceil(height / 512)
        return (tiles_x * tiles_y * cls.IMAGE_TILE_TOKENS) + cls.IMAGE_BASE_TOKENS

    @classmethod
    def estimate_audio(cls, duration_seconds: float) -> int:
        return max(1, math.ceil(duration_seconds * cls.AUDIO_TOKENS_PER_SECOND))

    @classmethod
    def estimate_video(cls, duration_seconds: float, fps: float = 1.0, width: int = 448, height: int = 448) -> int:
        frames = max(1, int(duration_seconds * fps))
        tokens_per_frame = cls.estimate_image(width, height, detail="low")
        return frames * tokens_per_frame


class MultimodalRouter:
    def __init__(self, max_context_tokens: int = 8192):
        self.max_context_tokens = max_context_tokens
        self.estimator = ModalityTokenEstimator()

    def process_and_budget(self, request: MultimodalRequest) -> Tuple[bool, str, Dict[str, Any]]:
        total_tokens = 0
        breakdown = {}

        for p in request.payloads:
            if p.modality == ModalityType.TEXT:
                tokens = self.estimator.estimate_text(str(p.content))
            elif p.modality == ModalityType.IMAGE:
                w = p.metadata.get("width", 1024)
                h = p.metadata.get("height", 1024)
                detail = p.metadata.get("detail", "high")
                tokens = self.estimator.estimate_image(w, h, detail)
            elif p.modality == ModalityType.AUDIO:
                dur = float(p.metadata.get("duration_seconds", 5.0))
                tokens = self.estimator.estimate_audio(dur)
            elif p.modality == ModalityType.VIDEO:
                dur = float(p.metadata.get("duration_seconds", 10.0))
                fps = float(p.metadata.get("sample_fps", 1.0))
                tokens = self.estimator.estimate_video(dur, fps)
            else:
                tokens = 0

            p.estimated_tokens = tokens
            total_tokens += tokens
            breakdown[p.modality.value] = breakdown.get(p.modality.value, 0) + tokens

        if total_tokens > request.total_token_budget:
            return False, f"Exceeded request token budget: {total_tokens} > {request.total_token_budget}", breakdown

        if total_tokens > self.max_context_tokens:
            return False, f"Exceeded system max context limit: {total_tokens} > {self.max_context_tokens}", breakdown

        return True, "Request successfully validated and budgeted", breakdown

    def route_to_fusion(self, request: MultimodalRequest) -> Dict[str, Any]:
        valid, msg, breakdown = self.process_and_budget(request)
        if not valid:
            return {"status": "rejected", "reason": msg, "breakdown": breakdown}

        return {
            "status": "accepted",
            "request_id": request.request_id,
            "fusion_strategy": request.target_fusion.value,
            "total_tokens": sum(breakdown.values()),
            "token_breakdown": breakdown,
            "routed_backend": "vllm-multimodal-orchestrator",
            "timestamp": time.time()
        }


if __name__ == "__main__":
    router = MultimodalRouter(max_context_tokens=8192)
    payloads = [
        ModalityPayload(ModalityType.TEXT, "Examine clinical lab report."),
        ModalityPayload(ModalityType.IMAGE, "lab_scan.png", {"width": 1280, "height": 960, "detail": "high"}),
        ModalityPayload(ModalityType.AUDIO, "doctor_voice.wav", {"duration_seconds": 18.5})
    ]
    req = MultimodalRequest("req-m06-d01-001", payloads, FusionStrategy.EARLY_FUSION, 4096)
    result = router.route_to_fusion(req)
    print("=== Multimodal Ingestion Routing Result ===")
    for k, v in result.items():
        print(f"{k}: {v}")
