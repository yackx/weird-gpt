# weird-gpt

**Experiments with OpenAI ChatGPT**

## Gist

A Python Streamlit web app for OpenAI ChatGPT experiments.

In some cases, a CLI is also available.

- **Weird assistants**: chatbots with tweaked prompts, some serious and some not.
- **Images**: create (and edit) images.
- **Moderation**: detect inputs that violate OpenAI rules (included in the weird assistants).

## Stack

- **Python 3.12**
- **[OpenAI ChatGPT](https://platform.openai.com)**
- **[streamlit](https://streamlit.io/)** (web app for weird assistants and images)

## Project structure

- [pages](pages) - Streamlit web app pages
- [weird_gpt](weird_gpt) - Chat and assistant logic 

## Install

```bash
$ python -m venv venv
$ source venv/bin/activate
(venv)$ pip install -r requirements.txt
```

## Dependencies

```bash
(venv)$ pip install pip-tools
(venv)$ pip-compile requirements.in  # generate requirements.txt
(venv)$ pip-compile requirements.in --upgrade  # upgrade dependencies list
(venv)$ pip install -r requirements.txt  # do not forget to actually upgrade
```

## Run from CLI

Each experiment has a separate basic CLI. Example:

```bash
python -m weird_gpt.moderation
```

## Run webapp

The main streamlit web app is in `Weird_GPT.py` (the unusual file name casing is part of streamlit conventions).

It requires:

- A valid OpenAI API key in `OPENAI_API_KEY` environment variable.
- A unique password to protect the application in `WEIRD_GPT_PASSWORD` environment variable.

```bash 
export WEIRD_GPT_PASSWORD=some_password
export OPENAI_API_KEY=sk-...
streamlit run Weird_GPT.py --browser.gatherUsageStats false --server.headless true
```

For production:

```bash
streamlit run Weird_GPT.py \
  --browser.gatherUsageStats false \
  --server.headless true \
  --server.fileWatcherType none \
  --client.toolbarMode minimal \
  --client.showErrorDetails false
```

![Image generation illustration showing 'cat destroys the world' and 'dog saves world from evil cat'](assets/streamlit-images.png)
