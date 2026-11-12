"""
Byte-Pair Encoding (BPE) Tokenizer Pretraining: Raw Corpus Frequency Counting,
Iterative Pair Merges, Special Token Handling, and Encoding/Decoding Engine.
"""

from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class BPETokenizer:
    vocab: Dict[int, bytes] = field(default_factory=dict)
    merges: Dict[Tuple[bytes, bytes], int] = field(default_factory=dict)
    special_tokens: Dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        if not self.vocab:
            # Initialize with 256 individual bytes
            for i in range(256):
                self.vocab[i] = bytes([i])

    def train(self, text: str, target_vocab_size: int, special_tokens: List[str] = None):
        if special_tokens:
            for st in special_tokens:
                st_id = len(self.vocab)
                self.special_tokens[st] = st_id
                self.vocab[st_id] = st.encode("utf-8")

        # Represent text as list of integer byte tokens
        tokens = list(text.encode("utf-8"))
        num_merges = target_vocab_size - len(self.vocab)

        for i in range(num_merges):
            if len(tokens) < 2:
                break
            pairs = Counter(zip(tokens[:-1], tokens[1:]))
            if not pairs:
                break
            best_pair = max(pairs, key=pairs.get)
            new_id = len(self.vocab)
            
            # Record merge
            pair_bytes = (self.vocab[best_pair[0]], self.vocab[best_pair[1]])
            self.merges[pair_bytes] = new_id
            self.vocab[new_id] = self.vocab[best_pair[0]] + self.vocab[best_pair[1]]

            # Replace pair in token stream
            new_tokens = []
            idx = 0
            while idx < len(tokens):
                if idx < len(tokens) - 1 and (tokens[idx], tokens[idx + 1]) == best_pair:
                    new_tokens.append(new_id)
                    idx += 2
                else:
                    new_tokens.append(tokens[idx])
                    idx += 1
            tokens = new_tokens

    def encode(self, text: str) -> List[int]:
        # Handle special tokens
        for st, st_id in self.special_tokens.items():
            if text == st:
                return [st_id]

        tokens = list(text.encode("utf-8"))
        # Iteratively apply merges
        while len(tokens) >= 2:
            pairs = list(zip(tokens[:-1], tokens[1:]))
            # Find earliest learned merge
            merge_candidates = []
            for pair in pairs:
                pair_bytes = (self.vocab[pair[0]], self.vocab[pair[1]])
                if pair_bytes in self.merges:
                    merge_candidates.append((self.merges[pair_bytes], pair))
            if not merge_candidates:
                break
            # Pick pair with smallest new_id (learned earliest)
            best_new_id, target_pair = min(merge_candidates, key=lambda x: x[0])
            
            new_tokens = []
            idx = 0
            while idx < len(tokens):
                if idx < len(tokens) - 1 and (tokens[idx], tokens[idx + 1]) == target_pair:
                    new_tokens.append(best_new_id)
                    idx += 2
                else:
                    new_tokens.append(tokens[idx])
                    idx += 1
            tokens = new_tokens
        return tokens

    def decode(self, token_ids: List[int]) -> str:
        byte_chunks = [self.vocab[t] for t in token_ids]
        return b"".join(byte_chunks).decode("utf-8", errors="replace")


if __name__ == "__main__":
    corpus = "low lower newest widest lowest low low lower newest"
    tokenizer = BPETokenizer()
    tokenizer.train(corpus, target_vocab_size=265, special_tokens=["<|endoftext|>"])

    encoded = tokenizer.encode("lowest")
    decoded = tokenizer.decode(encoded)
    print("Corpus:", corpus)
    print("Encoded 'lowest':", encoded)
    print("Decoded:", decoded)
    assert decoded == "lowest"
    assert "<|endoftext|>" in tokenizer.special_tokens
    print("Day 01 BPE Tokenizer Trainer verification passed.")
