import re

from config import CHUNK_SIZE, CHUNK_OVERLAP


def clean_text(text):

    text = re.sub(r"\s+", " ", text)

    text = re.sub(
        r"[^\w\s.,;:!?()%-]",
        " ",
        text
    )

    return text.strip()


def create_chunks(pages, source):

    chunks = []

    chunk_id = 0

    for page_data in pages:

        page_number = page_data["page"]

        text = clean_text(
            page_data["text"]
        )

        words = text.split()

        start = 0

        while start < len(words):

            end = start + CHUNK_SIZE

            chunk_words = words[start:end]

            chunk_text = " ".join(
                chunk_words
            )

            if len(chunk_text.strip()) > 30:

                chunks.append({
                    "id": chunk_id,
                    "source": source,
                    "page": page_number,
                    "text": chunk_text
                })

                chunk_id += 1

            start += (
                CHUNK_SIZE -
                CHUNK_OVERLAP
            )

    return chunks