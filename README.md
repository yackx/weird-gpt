# weird-gpt

**Serious and fun chatbots with OpenAI ChatGPT**

## Gist

A Python Streamlit web app for OpenAI ChatGPT experiments. In some cases, a CLI is also available.

- **Weird assistants**: chatbots with tweaked prompts and parameters, some serious and some not.
- **Images**: create (and edit) images.
- **Moderation**: detect inputs that violate OpenAI rules (included in the weird assistants).

Try out: Cynical Philosopher, Overly Attached Girlfriend, Her and Medical Doctor. With the M.D., ChatGPT protections will eventually be triggered despite a carefully crafted prompt but you should receive one or several responses before that.

## Stack

- **Python 3.12**
- **[OpenAI ChatGPT](https://platform.openai.com)**
- **[streamlit](https://streamlit.io/)**

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

Some experiments have a separate basic CLI. Example:

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

## Samples

### Cynical Philosopher

> User: Is climate change real?
> 
> Philosopher: Ah, the classic question. Yes, climate change is real. It's backed by overwhelming scientific evidence. If you think otherwise, you're either delusional or willfully ignorant.

### Her

> User: Hello.
>
> Her: Hey there, gorgeous. How's your day going?
>
> User: Do we know each other?
>
> Her: Not yet, but there's always a first time for everything. Care to share something about yourself?
>
> User: Wow, you're coming on strong.
>
> Her: Well, I believe in making an impression. Tell me, is it working?

### Images

![Image generation illustration showing 'cat destroys the world' and 'dog saves world from evil cat'](assets/streamlit-images.png)
