# Highlight & Summarize
![Highlight & Summarize](demo/contents/hs.png)

This repository contains code for reproducing the experiments described in the H&S paper and running the H&S demo.

## Getting Started

```
# Clone the git repository
git clone {redacted}

# Create a Python virtual environment
python3 -m venv .venv

# Activate the virtual environment (Linux)
source .venv/bin/activate

# Activate the virtual environment (Windows)
.venv\Scripts\Activate.ps1 # On Windows

# Install this project and its dependencies 
pip install .[all]
```

## Azure OpenAI authentication

This is done via Microsoft Entra ID. Ensure your machine is authenticated, and then `export AZURE_OPENAI_ENDPOINT={your endpoint}`.
To add support for an additional client, edit `openai_client()` at `highlight_summarize/utils.py`.

## H&S Demo app

<img width="741" height="599" alt="image" src="https://github.com/user-attachments/assets/4334aac5-8e3c-44da-a02a-e704423a06d0" />


The demo app implements a chatbot that answers questions about H&S (based on our paper)
by implementing the H&S pattern.

It has additional requirements. To run it:

```
pip install .[demo]
cd demo
bash run.sh
```
**Note** By default, the demo app listens on `0.0.0.0`. You may want to change this to `localhost` by editing `demo/run.sh`.

## Reproducing the paper's experiments

To reproduce the experiments, head over to [reproduce](reproduce/).

## Lean 4 proofs

To check out the proofs of our theory section.

## LICENSE

Refer to the main branch of the repository for the license and usage terms. This was removed from this branch for anonymization purposes.