# AI Basics Lab

A tiny, local-first project for learning AI concepts by trying them. It uses
Python's standard library and [Ollama](https://ollama.com/) with the small
`qwen3:0.6b` model. After setup, prompts and notes stay on your Mac.

## Start

Install Ollama from <https://ollama.com/download/mac> if it is not already
installed. This checkout also has an ignored, verified standalone runtime in
`.tools/ollama/`. The commands below use that runtime when present and the
installed `ollama` command on a fresh clone:

   ```sh
   ollama_bin=ollama
   [ -x .tools/ollama/ollama ] && ollama_bin="$PWD/.tools/ollama/ollama"
   OLLAMA_NO_CLOUD=1 OLLAMA_MODELS="$PWD/.models" "$ollama_bin" serve
   ```

   In a second Terminal window, from this folder, create the Python environment,
   download the chat and embedding models once, then index the OU PDFs:

   ```sh
   ollama_bin=ollama
   [ -x .tools/ollama/ollama ] && ollama_bin="$PWD/.tools/ollama/ollama"
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   OLLAMA_NO_CLOUD=1 OLLAMA_MODELS="$PWD/.models" "$ollama_bin" pull qwen3:0.6b
   OLLAMA_NO_CLOUD=1 OLLAMA_MODELS="$PWD/.models" "$ollama_bin" pull all-minilm
   .venv/bin/python study.py index "/path/to/OU"
   .venv/bin/python study.py lessons
   .venv/bin/python study.py ask "Explain AI inference in one paragraph"
   ```

Ollama listens on `http://localhost:11434`. No account or API key is needed.
On another Mac, install Ollama from <https://ollama.com/download/mac>, then use
`OLLAMA_NO_CLOUD=1 ollama serve` and pull both `qwen3:0.6b` and `all-minilm`
instead.

## Add your Oracle University PDFs

PDF indexing extracts the text locally, creates overlapping passages, asks
the local `all-minilm` embedding model for vectors, and stores those vectors
with source/page metadata in the embedded SQLite vector database. It does not
copy or change the original PDFs. To rebuild the index:

```sh
.venv/bin/python study.py index "/path/to/OU"
.venv/bin/python study.py search "redo generation and checkpointing"
.venv/bin/python study.py rag "What does the recovery layer do?"
```

Extracted text and the database file are under `.knowledge/` and excluded from
Git. Only PDF text is indexed; SQL, shell scripts, connection files, logs, and
other files are left alone. Ollama cloud features are disabled by the command
above. `sqlite-vec` is a small MIT/Apache-2.0 embedded SQLite vector extension;
it is pre-v1, which is fine for this learning project.

## Try the concepts

```sh
.venv/bin/python study.py search "why does retrieval help?"  # see ranked note snippets
.venv/bin/python study.py rag "How is RAG different from fine-tuning?" # retrieve, then generate
.venv/bin/python study.py react "What does an embedding do?" # inspect a simple tool/action/observation loop
```

`search` and `rag` use vector similarity. Use `keyword-search` to compare with
the earlier plain keyword-overlap baseline. `react` shows the loop explicitly:
choose the search tool, inspect its observation, then ask the model to answer
from the result. It logs actions and observations, not private chain-of-thought.

## Learning path

1. **Inference:** `ask` sends a prompt to a model and displays its output.
2. **Retrieval and RAG:** compare `ask` with `rag`; RAG adds selected note text
   to the prompt and asks for source labels.
3. **Embeddings and vectors:** `all-minilm` represents each passage and query
   as a vector. `sqlite-vec` stores vectors in a local SQLite file and ranks
   neighbors by cosine distance. A vector is useful for comparing meaning; it
   is not a database of exact facts.
4. **ReAct:** `react` makes a tool step visible. The model can use a tool's
   observation in its final response; a real agent needs strict tool limits.
5. **Fine-tuning:** later, compare a few labeled examples with RAG. Fine-tuning
   changes model behavior; it is usually not the best way to keep a changing
   reference library up to date.
6. **Causation:** run a controlled comparison: ask the same questions with
   retrieval on and off, change only that one factor, and score answers against
   known facts. Repeat questions and keep model, prompt, and scoring fixed.
   This helps test whether retrieval caused an improvement in this experiment;
   one run does not establish a universal claim.
7. **Chunks and context:** documents are split into passages for search. The
   model can only consider a limited amount of text at once, so chunk size and
   how much context is added both matter.
8. **Hallucinations and evaluation:** a confident answer can still be wrong.
   Check whether the retrieved passage supports the answer, and score retrieval
   quality separately from answer quality using a few questions with known
   answers.
9. **Prompts and agents:** prompts provide instructions and context. An agent
   wraps a model in a tool-use loop; tools need limits because they can take
   actions. Temperature changes output variety, not factual knowledge.

For a guided explanation of these ideas, continue with steps 7–11 in
[`LESSONS.md`](LESSONS.md).

## Next chapters: LangChain, LangGraph, and LangSmith

These are optional next steps after you understand the current local RAG flow.
The existing lab remains small and runs locally; the chapters explain how to
grow it without requiring these frameworks in the starter setup.

1. [Chapter 1: LangChain](chapters/01-langchain.md) — connect reusable pieces
   such as prompts, models, document loaders, embeddings, and retrievers.
2. [Chapter 2: LangGraph](chapters/02-langgraph.md) — turn a fixed sequence
   into a workflow with steps, shared state, and explicit choices.
3. [Chapter 3: LangSmith](chapters/03-langsmith.md) — inspect runs and evaluate
   answer quality; tracing is an optional observability step.

## Notes and privacy

The sample notes in `notes/` are the searchable knowledge base. Add small plain
text or Markdown files there. The current tool sends the selected note snippets
along with your question to the local Ollama service. Avoid putting secrets or
confidential data in the notes. This starter does not upload prompts or notes to
a cloud model provider.

## Troubleshooting

- If you see a connection error, start the local Ollama service in another terminal.
- If a model is missing, pull it with the local command above; `search` and
  `rag` need both `all-minilm` and the local Ollama service.
- If answers are weak, that is expected of a 0.6B model; try clearer questions
  and inspect what retrieval found before blaming the model.
