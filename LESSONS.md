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

## 7. What happens to a question?

Run `.venv/bin/python study.py rag "How does a database checkpoint work?"`.
Follow the path: your words become tokens, the app searches for relevant
passages, those passages and your question fit into the model's context, and
the model generates an answer. The model is only one part; the search, prompt,
PDF reader, and user interface are parts of the application around it.

## 8. Chunking and context limits

Documents are split into chunks so search can find a useful passage instead of
feeding a whole book to the model. Overlap keeps a little text from the end of
one chunk at the start of the next, helping preserve meaning across boundaries.
Very small chunks can lose context; very large chunks can bury the useful part.
Models also have a context limit: the total amount of text they can consider at
once. Try searching for a specific fact and inspect the returned source/page.

## 9. Hallucinations and checking sources

A fluent answer can still be wrong. In RAG, check whether the retrieved source
actually supports each important claim. If search returns weak passages, the
model may guess or combine unrelated details. Try `search` first, then `rag`,
and compare the answer to the source. Treat a citation as a pointer to check,
not proof by itself.

## 10. Evaluate the whole system

Keep a small list of questions and known answers. For each question, record:
whether search found the right passage, whether the answer is correct, and
whether the cited source supports it. Search quality and answer quality are
different: a good model cannot use a passage that retrieval missed. Change one
thing at a time (for example, chunk size or prompt wording) to learn what helped.

## 11. Prompts, settings, and agents

A prompt is the instruction and context sent to a model. Clear instructions,
relevant examples, and useful source text can improve results without changing
the model's parameters. Temperature is a generation setting that affects how
varied outputs are; it does not make an answer more knowledgeable or factual.
An agent adds a loop around a model so it can choose tools and use their results.
Start with read-only tools and explicit limits, because a tool may have real
side effects.
