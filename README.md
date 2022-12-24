# HowdoI.ai is a helpful chatbot that can answer questions

This is an experiment in building a large-language-model-backed chatbot. It can hold a conversation, remember previous comments/questions, and answer all types of queries (history, web search, movie data, weather, news, and more).

This app relies on the amazing [LangChain Python library](https://langchain.readthedocs.io/en/latest/index.html), which powers all the interesting AI stuff.

## Running locally

First, add your API keys in the `.env` file.

Then, install the Python requirements and start the app. You'll want a Procfile manager like [Foreman](https://github.com/ddollar/foreman) or [Hivemind](https://github.com/DarthSim/hivemind) installed.

```
pip install requirements.txt
foreman start -f Procfile.local
```

Once it's running, open up [http://127.0.0.1:9000/](http://127.0.0.1:9000/) and you'll be able to start interacting with the bot. There's also a writing assistant endpoint at [http://127.0.0.1:9000/write](http://127.0.0.1:9000/write).

## Example prompts

### Conversation with memory

`hi, my name is bob`

`Hi Bob! Nice to meet you! How can I help you today?`

`what's the last letter of my name?`

`b`

## Deploying

This repository is set up to deploy on [Fly.io](https://fly.io/). You should be able to follow [their docs and get it running there very quickly](https://fly.io/docs/languages-and-frameworks/python/).

## Experiments Folder

This folder has a few attempts at generating/testing LLM examples programmatically. You can probably ignore this unless you're just curious.
