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
