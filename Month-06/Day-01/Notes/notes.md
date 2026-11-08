# Engineering Notes — Day 01: Multimodal Architecture & Tokenization Math
- ViT Patch tokens: $N = \frac{H \times W}{P^2}$. For $448 \times 448$ at $P=14$, $N=1,024$.
- Dynamic tiling downsamples full image and adds $512 \times 512$ local crops at 170 tokens/tile.
- Audio tokenization: $12.5$ tokens per second of raw audio waveform.
