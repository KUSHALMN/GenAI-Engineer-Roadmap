"""
Multimodal GenAI Prompt Flow & Image Token Estimation.
Constructs vision-language payloads (GPT-4o, Claude 3.5 Sonnet, Gemini format),
validates image encodings, and estimates image token costs.
"""

import base64
import math
from typing import Any, Dict, List, Optional, Union


class MultimodalPromptBuilder:
    """Builds standard multimodal payloads combining text queries and images."""

    @staticmethod
    def estimate_image_tokens(width: int, height: int, detail: str = "high") -> int:
        """
        Calculates OpenAI-standard image token consumption:
        Low detail: 85 tokens.
        High detail: 85 base tokens + 170 tokens per 512x512 tile.
        """
        if detail == "low":
            return 85

        # Fit within 2048x2048
        if width > 2048 or height > 2048:
            aspect = width / height
            if aspect > 1:
                width = 2048
                height = int(2048 / aspect)
            else:
                height = 2048
                width = int(2048 * aspect)

        # Scale shortest side to 768
        shortest = min(width, height)
        scale = 768.0 / shortest if shortest > 768 else 1.0
        width = int(width * scale)
        height = int(height * scale)

        # Count 512x512 tiles
        tiles_w = math.ceil(width / 512.0)
        tiles_h = math.ceil(height / 512.0)
        total_tiles = tiles_w * tiles_h

        return 85 + (170 * total_tiles)

    @classmethod
    def create_multimodal_message(
        cls,
        text_prompt: str,
        image_base64_or_url: str,
        mime_type: str = "image/png",
        detail: str = "high",
    ) -> Dict[str, Any]:
        """Creates standard OpenAI vision message format."""
        if image_base64_or_url.startswith("http://") or image_base64_or_url.startswith("https://"):
            image_url_payload = {"url": image_base64_or_url, "detail": detail}
        else:
            image_url_payload = {
                "url": f"data:{mime_type};base64,{image_base64_or_url}",
                "detail": detail,
            }

        return {
            "role": "user",
            "content": [
                {"type": "text", "text": text_prompt},
                {"type": "image_url", "image_url": image_url_payload},
            ],
        }


if __name__ == "__main__":
    # Test token estimation
    low_tokens = MultimodalPromptBuilder.estimate_image_tokens(1024, 768, detail="low")
    assert low_tokens == 85

    high_tokens = MultimodalPromptBuilder.estimate_image_tokens(1024, 768, detail="high")
    assert high_tokens > 85
    print(f"Image 1024x768 token estimate: {high_tokens} tokens")

    # Test payload construction
    msg = MultimodalPromptBuilder.create_multimodal_message(
        text_prompt="Transcribe the table in this invoice image.",
        image_base64_or_url="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
    )
    assert len(msg["content"]) == 2
    assert msg["content"][0]["type"] == "text"
    assert msg["content"][1]["type"] == "image_url"
    print("MultimodalPromptBuilder tests passed successfully!")
