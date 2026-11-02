# AI basics

Inference is running a trained model on an input to produce an output. It does
not update the model's learned parameters.

An embedding is a list of numbers representing a piece of text. Texts with
related meanings can have vectors that are close under a similarity measure.
Vector search ranks stored vectors by similarity to a query vector.

Retrieval augmented generation, or RAG, retrieves relevant reference text and
includes it in the prompt sent to a language model. The retrieved text can
ground an answer, but retrieval errors can lead to poor answers.

Fine-tuning updates a model using training examples. It can teach patterns or
style, but is not the same as looking up changing reference information.

Causation means one factor produces a change in an outcome. A controlled
experiment changes one factor while keeping other conditions as similar as
possible. Correlation alone does not prove causation.

ReAct is a pattern combining reasoning steps with actions such as calling a
search tool, observing its result, and then continuing. Tool permissions and
limits matter because an agent can take actions beyond text generation.

## More useful ideas

A token is a small piece of text a model processes. It may be a word, part of a
word, or punctuation. A model's context window is the maximum amount of input
and generated text it can handle in one go.

Chunking splits long documents into smaller passages for retrieval. Overlap
repeats a little text between neighboring passages to reduce the chance that a
sentence or idea is cut apart. Small chunks are precise but may lack context;
large chunks have context but can include distracting material.

Hallucination is when a model produces an unsupported or incorrect claim,
sometimes in a confident tone. RAG can reduce this risk when it retrieves good
evidence, but it cannot guarantee correctness. Open the source and verify.

Evaluation means checking system behavior against questions with known answers.
Measure whether search found the right passage separately from whether the
model answered correctly. This helps locate whether a problem came from
retrieval, the prompt, or generation.

A prompt is the instruction and context supplied to the model. Temperature is
a setting that changes how varied the generated wording may be; it does not add
knowledge or guarantee truth. An AI application combines a model with other
parts such as prompts, document readers, search, and a user interface. An agent
adds a loop that lets the model use tools, so tools should have clear limits.
