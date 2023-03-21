# HowdoI.ai is a helpful chatbot that can answer questions

This is an experiment in building a large-language-model-backed chatbot. It can hold a conversation, remember previous comments/questions, and answer all types of queries (history, web search, movie data, weather, news, and more).

This app relies on the amazing [LangChain Python library](https://langchain.readthedocs.io/en/latest/index.html), which powers all the interesting AI stuff.

## Running locally

First, add your API keys in the `.env` file.

Install the NPM requirements:

```
cd vite
npm install (or yarn install)
```

Then, install the Python requirements and start the app. You'll want a Procfile manager like [Foreman](https://github.com/ddollar/foreman) or [Hivemind](https://github.com/DarthSim/hivemind) installed.

```
pip install -r requirements.txt
foreman start -f Procfile.local
```

(Note: foreman isn't required. You can run the commands in the Procfile.local in separate terminal windows if you prefer)

Once it's running, open up [http://127.0.0.1:9000/](http://127.0.0.1:9000/) and you'll be able to start interacting with the bot. There's also a writing assistant endpoint at [http://127.0.0.1:9000/write](http://127.0.0.1:9000/write).

## Example prompts

### Conversation with memory

Q: `hi, my name is bob`

A: `Hi Bob! Nice to meet you! How can I help you today?`

Q: `what's the last letter of my name?`

A: `b`

Q: `show me a cat gif`

A: `Here is a cat gif: <iframe src="https://giphy.com/embed/ICOgUNjpvO0PC" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><br /><a href="https://giphy.com/embed/ICOgUNjpvO0PC">powered by GIPHY</a>`

Q: `actually, can you make it a dolphin?`

A: `Here is a dolphin gif: <iframe src="https://giphy.com/embed/11ctq1pDmD3cB2" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><br /><a href="https://giphy.com/embed/11ctq1pDmD3cB2">powered by GIPHY</a>`

### Movies

Q: `what year was Dr. Strangelove released?`

A: `Dr. Strangelove was released in 1964.`

### Math

Q: `what's the sum of the first six prime numbers?`

A: `The sum of the first six prime numbers is 41.`

## Deploying

This repository is set up to deploy on [Fly.io](https://fly.io/). You should be able to follow [their docs and get it running there very quickly](https://fly.io/docs/languages-and-frameworks/python/).

## Experiments Folder

This folder has a few attempts at generating/testing LLM examples programmatically. You can probably ignore this unless you're just curious.
