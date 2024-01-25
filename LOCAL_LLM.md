## Experimental feature

SemanticShield can be used with a local LLM for functionality, but still relies on the OpenAI moderation functionality


## Setup

Install local LLM (e.g. [ollama](https://ollama.ai/), [LM Studio](https://lmstudio.ai/))

Download/install/run your prefered model (see the respective documentations)

For ollama ou will also require a proxy, such as [LiteLLM proxy](https://github.com/BerriAI/litellm?tab=readme-ov-file#openai-proxy---docs)

Set the LOCAL_BASE_URL environment variable to point to your local LLM/proxy
- e.g. ```export LOCAL_BASE_URL=http://localhost:1234/v1``` for LM Studio

