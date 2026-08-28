from typing import List, Dict, Any

class RecursiveChunker:
    """
    Intelligent Recursive Character Text Splitter that preserves document structure,
    paragraph boundaries, sentence integrity, and page-level metadata.
    """

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be strictly less than chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = ["\n\n", "\n", ". ", "; ", ", ", " "]

    def split_pages(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Split a list of page objects into overlapping text chunks with enriched metadata.
        """
        chunks = []
        chunk_global_id = 0

        for page in pages:
            page_num = page.get("page_number", 1)
            source = page.get("source", "unknown")
            page_text = page.get("text", "")

            page_chunks = self._split_text(page_text)
            for idx, text in enumerate(page_chunks):
                chunk_id = f"{source}_p{page_num}_c{idx}"
                chunks.append({
                    "chunk_id": chunk_id,
                    "global_id": chunk_global_id,
                    "text": text,
                    "source": source,
                    "page_number": page_num,
                    "chunk_index": idx,
                    "char_count": len(text),
                    "word_count": len(text.split())
                })
                chunk_global_id += 1

        return chunks

    def _split_text(self, text: str) -> List[str]:
        if not text or len(text) <= self.chunk_size:
            return [text] if text else []

        raw_splits = self._recursive_split(text, self.separators)
        
        # Merge splits into windows with overlap
        merged_chunks = []
        current_chunk = []
        current_length = 0

        for split in raw_splits:
            split_len = len(split)
            if current_length + split_len > self.chunk_size and current_chunk:
                merged_chunks.append("".join(current_chunk).strip())
                
                # Keep overlap items from the end of current_chunk
                overlap_chunk = []
                overlap_len = 0
                for item in reversed(current_chunk):
                    if overlap_len + len(item) <= self.chunk_overlap:
                        overlap_chunk.insert(0, item)
                        overlap_len += len(item)
                    else:
                        break
                current_chunk = overlap_chunk
                current_length = overlap_len

            current_chunk.append(split)
            current_length += split_len

        if current_chunk:
            final_text = "".join(current_chunk).strip()
            if final_text:
                merged_chunks.append(final_text)

        return merged_chunks

    def _recursive_split(self, text: str, separators: List[str]) -> List[str]:
        """Recursively break down text by prioritized separator."""
        final_pieces = []
        separator = separators[-1]
        new_separators = []

        for i, sep in enumerate(separators):
            if sep == "":
                separator = ""
                break
            if sep in text:
                separator = sep
                new_separators = separators[i + 1:]
                break

        splits = text.split(separator) if separator else list(text)
        for s in splits:
            if not s:
                continue
            if separator and separator != "":
                s = s + separator

            if len(s) <= self.chunk_size:
                final_pieces.append(s)
            else:
                if new_separators:
                    sub_pieces = self._recursive_split(s, new_separators)
                    final_pieces.extend(sub_pieces)
                else:
                    # Character slice fallback
                    for start_idx in range(0, len(s), self.chunk_size):
                        final_pieces.append(s[start_idx:start_idx + self.chunk_size])

        return final_pieces
