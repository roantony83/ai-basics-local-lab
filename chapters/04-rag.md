# Chapter 4: RAG — let the model consult your material

RAG means **retrieval-augmented generation**. Think of an open-book question:
the app first finds relevant pages, then gives those pages to the model while
it writes an answer.

## The two main stages

1. **Retrieve:** turn the question into an embedding and search for related
   chunks in the vector database.
2. **Generate:** add the selected chunks to the prompt and ask the language
   model to answer using that context.

The retrieved material augments the model's prompt. It does not retrain the
model. RAG can help answer questions about your documents, but it cannot
guarantee correctness: retrieval may find the wrong passage, and a model may
misread or overstate what the source says.

## Try the three views

Use the same question for each command:

```sh
.venv/bin/python study.py ask "What does my training material say about checkpoints?"
.venv/bin/python study.py search "What does my training material say about checkpoints?"
.venv/bin/python study.py rag "What does my training material say about checkpoints?"
```

- `ask` answers from the model without searching your indexed materials.
- `search` shows the passages the retriever found.
- `rag` shows those passages, then asks the model to answer from them.

Check whether the answer is supported by the passages, not just whether it
sounds confident. A source label is a pointer to inspect, not proof by itself.

## Learn more

- [Official LangChain learning tutorials](https://docs.langchain.com/oss/python/learn)
