# Chapter 2: LangGraph — make the workflow visible

## The idea

A straight RAG program follows a sequence: find passages, then ask the model
for an answer. LangGraph helps describe workflows that have several steps,
keep information between steps, or need to choose what happens next.

Think of a flowchart where each box does one job. In LangGraph, a box is a
**node**, the arrows are **edges**, and the shared notebook that nodes read and
update is **state**. Some edges can be chosen conditionally.

## A learning graph for this lab

```text
START → retrieve passages → are useful passages found?
                              ├─ no → explain that the notes do not answer → END
                              └─ yes → generate cited answer → END
```

Possible state fields are the question, retrieved passages, and final answer.
For this beginner workflow, the nodes should be simple and understandable:

1. **Retrieve:** call the same local vector search already used by `study.py`.
2. **Check:** see whether any passages were returned (later, evaluate their
   relevance more carefully).
3. **Generate:** use the local Ollama model with the selected passages.
4. **Finish:** return the answer or a clear no-evidence response.

This is workflow control, not a new language model. LangGraph is useful when
the path needs branches, retries, saved progress, or a human approval step.

## Small exercise

Draw the current `rag` command as boxes and arrows. Then add one branch for
"no passages found." Identify what data must travel from retrieval to
generation. That data is a first draft of graph state.

Do not add tools that change files or contact external services in the first
graph. Start with local, read-only retrieval and visible steps.

## Learn more

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [Think in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)
