# Chapter 1: Chunking — split documents into useful pieces

## The idea

Imagine looking for one fact in a 500-page book. It is easier if the book has
been divided into small cards, each holding one passage. In a RAG project,
those passages are called **chunks**.

Chunks are made before search. A chunk should be large enough to explain an
idea, but small enough that search can pick the useful part without bringing
along a whole chapter. Neighboring chunks can overlap, so a sentence near a
boundary is less likely to lose its context.

## In this project

`study.py` reads extracted PDF text page by page. It makes chunks of up to 180
words, starting a new chunk every 140 words. That means neighboring chunks
share about 40 words. The project keeps the source filename and page number so
search results can point back to where the text came from.

The sample notes in `notes/` are also included in the index. If you change the
PDFs or notes, run `study.py index <folder>` again to rebuild the index.

## Small exercise

Run a search for a topic from a training PDF and inspect its result. Ask:

- Does the passage make sense by itself?
- Would a little text before or after it help?
- Is it focused, or does it contain several unrelated topics?

There is no perfect chunk size for every document. Tables, code, slides, and
prose may need different handling.
