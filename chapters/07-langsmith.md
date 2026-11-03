# Chapter 7: LangSmith — see and evaluate what happened

## The idea

When an AI answer is weak, it helps to see the steps that produced it. LangSmith
is an observability and evaluation platform from LangChain. It can show a run's
inputs, outputs, intermediate steps, and timing, and help compare answers
against a set of example questions and expected results.

For this lab, imagine inspecting a run and asking:

- Did retrieval find the right passage?
- Did the model receive the passage and question we expected?
- Did the final answer match the source?
- Did a code or configuration change make answers better or worse?

The current project already prints search results before the RAG answer. That
is a simple, local form of observability. Its manual question-and-answer
comparison is a simple evaluation. LangSmith can make those practices easier
to inspect and repeat across many runs.

## Optional and privacy-aware

LangSmith tracing is **not enabled** in this starter project. Using the hosted
service involves sending trace data to LangSmith. Traces may contain questions,
retrieved document text, and model answers, so use only material you are
permitted to share and review the current configuration before turning tracing
on. LangSmith also documents self-hosted options, which require additional
infrastructure and are beyond this beginner lab.

You can learn the ideas without creating an account or sending any data. First
keep a small local evaluation list with a question, expected facts, retrieved
source, and a correctness/support score. That is enough to learn what
observability and evaluation are for.

## Small exercise

Create three questions about your notes. For each, record:

| Question | Did search find useful evidence? | Is the answer correct? | Does the evidence support it? |
| --- | --- | --- | --- |
| Your question | Yes / No | Yes / No | Yes / No |

Keep retrieval quality separate from answer quality. If the right passage was
not retrieved, changing the prompt may not solve the real problem.

## Learn more

- [LangSmith observability](https://docs.langchain.com/langsmith/observability)
- [LangSmith evaluation types](https://docs.langchain.com/langsmith/evaluation-types)
- [LangSmith data plane and tracing choices](https://docs.langchain.com/langsmith/data-plane)
