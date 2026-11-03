# Chapter 2: Embeddings — turn meaning into numbers

## The idea

An **embedding** is a list of numbers made from a piece of text. An embedding
model tries to place passages with related meanings in similar regions of a
number space. This lets a computer compare meaning-like patterns, not just
look for identical words.

An embedding is not a dictionary, a summary, or a guaranteed understanding of
the text. It is a numerical representation that is useful for comparison.

## In this project

The local `all-minilm` model creates embeddings for each chunk and for your
search question. The same embedding model is used on both sides so the query
and stored passages can be compared. The chat model `qwen3:0.6b` has a
different job: it writes an answer after retrieval.

## Small exercise

Try these searches and compare the first result:

```sh
.venv/bin/python study.py search "What is an embedding?"
.venv/bin/python study.py search "How can software represent a sentence with numbers?"
```

If both find a useful passage, that shows how related wording can still lead
to a related result. It does not mean every result will be correct; inspect
the source text.

## Learn more

- [LangChain embeddings concepts](https://docs.langchain.com/oss/python/integrations/embeddings)
