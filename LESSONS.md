# First five-minute tour

## 1. Inference

Run `python3 study.py ask "Explain inference using a cooking analogy"`. Inference
means using a trained model to produce an output for an input. The model is not
being retrained by this request.

## 2. Search, vectors, and embeddings

Run `.venv/bin/python study.py search "find information about retrieval"` and
compare it with `keyword-search`. The embedding model maps text to a list of
numbers (a vector); `sqlite-vec` stores them in `.knowledge/vectors.sqlite` and
ranks nearby vectors using cosine distance. Lower distance means closer in
vector space. This is a local SQLite file, not a Pinecone cloud account.

## 3. RAG

Run the same question once with `ask` and once with `rag`. Retrieval augmented
generation (RAG) finds potentially useful text and adds it to the model input.
Compare the answers and check the cited note. Retrieval can help with local
reference material, but bad retrieval can supply irrelevant context.

## 4. ReAct

Run `python3 study.py react "What is RAG?"` and read the printed ACTION and
OBSERVATION. ReAct is short for a reasoning-and-action pattern: an AI uses a
tool, sees the result, and continues. Here the tool is deliberately fixed to
search. A real tool-using agent should have a narrow allowlist and limits.

## 5. Causation

Try this mini experiment after a few questions:

1. Write five answerable questions using only the notes.
2. For each, record an `ask` answer and a `rag` answer.
3. Score both against the same answer key for correctness and source support.
4. Change only retrieval; keep model, questions, and scoring the same.
5. Compare the scores. This is evidence about the effect of retrieval in this
   small setup, not proof that RAG always improves answers.

## 6. Fine-tuning

Fine-tuning changes model parameters using training examples. It can teach a
consistent style or task pattern, but needs carefully prepared examples and
more compute than this first lab. It is different from RAG: RAG supplies
reference material at answer time; fine-tuning changes the model itself. First
learn to measure a baseline before training anything.

## Oracle training PDFs

Index PDFs from a folder with `.venv/bin/python study.py index "/path/to/folder"`.
The PDF text is extracted locally, embedded by Ollama's `all-minilm` model,
then stored in `sqlite-vec` with page/source metadata. The originals are
read-only inputs; extracted text and vector database files are under
`.knowledge/`, excluded from Git.
