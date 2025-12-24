# utils/chunker.py

def chunk_text(text, max_length=300):
    """
    Splits text into chunks of max_length characters.
    """
    chunks = []
    words = text.split()
    current_chunk = []

    for word in words:
        if len(" ".join(current_chunk + [word])) <= max_length:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks