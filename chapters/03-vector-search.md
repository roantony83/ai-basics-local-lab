# Chapter 3: Vector search — find passages by similarity

## The idea

Once chunks have embeddings, a search system can compare your question's
embedding with the stored chunk embeddings. It returns chunks whose vectors
are closest according to a distance measure. In this project that measure is
cosine distance; **lower distance means a closer match**.

Vector search is different from keyword search. Keyword search looks for words
in common. Vector search compares embeddings, which can help when a question
uses different wording from the document. Neither method is always right.

## In this project

The embeddings and text are stored in `.knowledge/vectors.sqlite`. The
`sqlite-vec` extension lets SQLite search the vectors and return the closest
three chunks, along with their source and page information. This is a local
database file, not a hosted vector database.

## Small exercise

Run both commands with the same question:

```sh
.venv/bin/python study.py keyword-search "How does software find related ideas?"
.venv/bin/python study.py search "How does software find related ideas?"
```

Compare the results. Which one found a useful passage? Can you spot an
irrelevant result? The vector score is a ranking signal, not a correctness
score or a probability that the passage is right.

## Learn more

- [LangChain semantic search tutorial](https://docs.langchain.com/oss/python/learn)
