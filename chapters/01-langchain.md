# Chapter 1: LangChain — connect the AI building blocks

## The idea

The current `study.py` lab already performs a small RAG workflow. LangChain is
a framework that gives common AI application parts standard interfaces and
connects them together. It does not make a model smarter by itself.

Think of the project as a little workshop. The model is one tool; the prompt,
PDF reader, text splitter, embedding model, vector store, and retriever are
other tools. LangChain helps wire compatible tools into a repeatable process.

## Match it to this project

| Current lab part | Common LangChain idea |
| --- | --- |
| `PdfReader` in `study.py` | Document loader |
| `documents()` divides text into passages | Text splitter |
| `embed()` calls `all-minilm` | Embeddings interface |
| `sqlite-vec` table | Vector store |
| `search()` gets the closest passages | Retriever |
| `generate()` sends instructions to Ollama | Chat model and prompt |
| `rag` command joins retrieval and generation | RAG chain / runnable sequence |

Names and package boundaries can change between LangChain releases, so follow
the current official docs when you are ready to write code.

## Small exercise

1. Run `study.py search "How does a computer represent sentence meaning?"`.
2. Run `study.py rag` with the same question.
3. Point to the loader, splitter, embedding, vector store, retriever, prompt,
   and model in the table above.
4. Explain which parts LangChain could standardize and which part still does
   the actual answer generation.

The goal is not to replace working code immediately. First recognize that the
framework is organizing building blocks you have already seen.

## Learn more

- [LangChain Python documentation](https://docs.langchain.com/oss/python/langchain/overview)
- [Official learn tutorials](https://docs.langchain.com/oss/python/learn)
