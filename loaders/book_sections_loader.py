from pathlib import Path


def get_book_sections():
    files = [f for f in Path().glob("./data/sections_t20_livro/*.md")]

    texts = []
    metadatas = []
    for f in files:
        metadatas.append({"source": str(f)})
        texts.append(f.read_text(encoding='utf8'))

    return texts, metadatas