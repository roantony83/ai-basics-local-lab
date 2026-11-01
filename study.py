#!/usr/bin/env python3
"""Small, inspectable AI concepts lab using only Python's standard library."""

import json
import logging
import re
import sqlite3
import sys
import shutil
import warnings
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen
from pypdf import PdfReader
import sqlite_vec

logging.getLogger("pypdf").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", module="pypdf")

ROOT = Path(__file__).resolve().parent
NOTES = ROOT / "notes"
MODEL = "qwen3:0.6b"
EMBED_MODEL = "all-minilm"
OLLAMA_CHAT = "http://localhost:11434/api/chat"
OLLAMA_EMBED = "http://localhost:11434/api/embed"
VECTOR_DB = ROOT / ".knowledge" / "vectors.sqlite"
STOP = {"a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
        "how", "in", "is", "it", "of", "on", "or", "that", "the", "this",
        "to", "what", "when", "where", "why", "with"}


def words(text):
    return {word for word in re.findall(r"[a-z0-9]+", text.lower()) if word not in STOP}


def documents():
    result = [(path.name, path.read_text(encoding="utf-8"))
              for path in sorted(NOTES.glob("*.md"))]
    knowledge = ROOT / ".knowledge"
    if knowledge.exists():
        for path in sorted(knowledge.rglob("*.txt")):
            text = path.read_text(encoding="utf-8", errors="replace")
            label = str(path.relative_to(knowledge))
            pages = re.split(r"\[Page (\d+)\]", text)
            if len(pages) > 1:
                page_texts = [(pages[index], pages[index + 1])
                              for index in range(1, len(pages) - 1, 2)]
            else:
                page_texts = [("0", text)]
            for page, page_text in page_texts:
                tokens = page_text.split()
                for start in range(0, len(tokens), 140):
                    words = " ".join(tokens[start:start + 180]).strip()
                    if words:
                        marker = f"[Page {page}] " if page != "0" else ""
                        result.append((label, marker + words))
    return result


def index_pdfs(source):
    source = Path(source).expanduser().resolve()
    if not source.is_dir():
        raise SystemExit(f"Not a folder: {source}")
    destination = ROOT / ".knowledge" / "oracle-ou"
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)
    count = 0
    skipped = 0
    for pdf in sorted(source.rglob("*.pdf")):
        try:
            relative = str(pdf.relative_to(source)).replace("/", "_")
            target = destination / f"{relative}.txt"
            reader = PdfReader(str(pdf))
            if reader.is_encrypted and not reader.decrypt(""):
                raise ValueError("password protected")
            pages = []
            for page_number, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                if text.strip():
                    pages.append(f"\n[Page {page_number}]\n{text}")
            target.write_text("\n".join(pages), encoding="utf-8")
            count += 1
        except Exception as error:
            skipped += 1
            print(f"Skipped {pdf.name}: {type(error).__name__}", file=sys.stderr)
    if not count:
        raise SystemExit(f"No PDFs found under {source}")
    chunks = documents()
    build_vector_index(chunks)
    print(f"Read {count} PDFs; skipped {skipped}; stored {len(chunks)} text chunks and vectors in {VECTOR_DB}.")


def keyword_search(query, limit=3):
    query_terms = words(query)
    ranked = []
    for name, content in documents():
        terms = words(content)
        score = len(query_terms & terms)
        if score:
            ranked.append((score, name, content.strip()))
    return sorted(ranked, key=lambda item: (-item[0], item[1]))[:limit]


def embed(texts):
    request = Request(OLLAMA_EMBED,
                      data=json.dumps({"model": EMBED_MODEL, "input": texts}).encode(),
                      headers={"Content-Type": "application/json"})
    try:
        with urlopen(request, timeout=300) as response:
            return json.load(response)["embeddings"]
    except URLError as error:
        raise SystemExit("Can't reach local Ollama. Start it with OLLAMA_NO_CLOUD=1.\n"
                         f"Details: {error}") from error


def open_vector_db():
    if not VECTOR_DB.exists():
        raise SystemExit("Vector index is missing. Run `study.py index <folder-with-PDFs>` first.")
    connection = sqlite3.connect(VECTOR_DB)
    connection.enable_load_extension(True)
    sqlite_vec.load(connection)
    connection.enable_load_extension(False)
    return connection


def build_vector_index(chunks):
    if not chunks:
        raise SystemExit("No text chunks to index.")
    VECTOR_DB.parent.mkdir(parents=True, exist_ok=True)
    batches = [chunks[index:index + 32] for index in range(0, len(chunks), 32)]
    first_vectors = embed([content for _, content in batches[0]])
    dimension = len(first_vectors[0])
    connection = sqlite3.connect(VECTOR_DB)
    connection.enable_load_extension(True)
    sqlite_vec.load(connection)
    connection.enable_load_extension(False)
    connection.execute("DROP TABLE IF EXISTS vec_chunks")
    connection.execute(f"""CREATE VIRTUAL TABLE vec_chunks USING vec0(
        embedding float[{dimension}] distance_metric=cosine,
        source text,
        page integer,
        +content text
    )""")
    next_rowid = 1
    for batch_number, batch in enumerate(batches):
        vectors = first_vectors if batch_number == 0 else embed([content for _, content in batch])
        records = []
        for (name, content), vector in zip(batch, vectors):
            filename = name.rsplit("/", 1)[-1].removesuffix(".txt")
            page_match = re.search(r"\[Page (\d+)\]", content)
            page = int(page_match.group(1)) if page_match else 0
            records.append((next_rowid, sqlite_vec.serialize_float32(vector), filename, page, content))
            next_rowid += 1
        connection.executemany(
            "INSERT INTO vec_chunks(rowid, embedding, source, page, content) VALUES (?, ?, ?, ?, ?)",
            records)
        connection.commit()
        print(f"Embedded {min(next_rowid - 1, len(chunks))}/{len(chunks)} chunks", flush=True)
    connection.close()


def search(query, limit=3):
    query_vector = sqlite_vec.serialize_float32(embed([query])[0])
    try:
        with open_vector_db() as connection:
            rows = connection.execute("""SELECT source, page, content, distance
                FROM vec_chunks
                WHERE embedding MATCH ? AND k = ?
                ORDER BY distance""", (query_vector, limit)).fetchall()
    except sqlite3.OperationalError as error:
        raise SystemExit(f"Vector search failed: {error}") from error
    return [(distance, f"{source} (page {page})" if page else source, content)
            for source, page, content, distance in rows]


def show_results(results, score_label="cosine distance; lower is closer"):
    if not results:
        print("No matching notes. Try different keywords or add a note under notes/.")
        return
    for score, name, content in results:
        snippet = " ".join(content.split())
        print(f"[{name}] {score_label}={score:.4f}: {snippet[:420]}")


def generate(prompt):
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "think": False,
        "options": {"temperature": 0.2},
    }).encode()
    request = Request(OLLAMA_CHAT, data=body,
                      headers={"Content-Type": "application/json"})
    try:
        with urlopen(request, timeout=300) as response:
            result = json.load(response)
    except URLError as error:
        raise SystemExit("Can't reach local Ollama. Start `ollama serve` in another terminal.\n"
                         f"Details: {error}") from error
    print(result["message"]["content"].strip())


def usage():
    print("Usage: study.py {lessons|index|ask|keyword-search|search|rag|react} [question or folder]")
    raise SystemExit(2)


def main():
    if len(sys.argv) < 2:
        usage()
    command = sys.argv[1]
    if command == "lessons":
        print((ROOT / "LESSONS.md").read_text(encoding="utf-8"))
        return
    if command == "index":
        if len(sys.argv) != 3:
            usage()
        index_pdfs(sys.argv[2])
        return
    if command not in {"ask", "keyword-search", "search", "rag", "react"} or len(sys.argv) < 3:
        usage()
    question = " ".join(sys.argv[2:])

    if command == "ask":
        generate(question)
    elif command == "keyword-search":
        show_results(keyword_search(question), "keyword overlap; higher is more")
    elif command == "search":
        show_results(search(question))
    elif command == "rag":
        results = search(question)
        show_results(results)
        if results:
            context = "\n\n".join(f"Source {name}:\n{text}" for _, name, text in results)
            generate("Answer the question using only the supplied notes. If they do not "
                     "contain the answer, say so. Cite source filenames.\n\n"
                     f"NOTES:\n{context}\n\nQUESTION: {question}")
    else:
        print("Step 1 - ACTION: call the local search tool")
        results = search(question)
        print("Step 2 - OBSERVATION: search returned these snippets")
        show_results(results)
        if results:
            context = "\n\n".join(f"Source {name}:\n{text}" for _, name, text in results)
            print("Step 3 - ACTION: give the model the question and tool observation")
            generate("Use the tool observation to answer briefly. Cite source filenames; "
                     "if the notes do not answer the question, say so.\n\n"
                     f"TOOL OBSERVATION:\n{context}\n\nQUESTION: {question}")


if __name__ == "__main__":
    main()
