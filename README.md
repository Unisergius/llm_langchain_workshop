# LLM Langchain Workshop

Mini workshop guide to create simple apps that use llms with langchain. Based on Stephen Grider's Langchain workshop in Udemy.

## What we're going to do

We are going to do 3 different apps with langchain:

1. Simple Chat Application: This app will serve as a small introduction to the concept of prompts and demonstrate the importance of providing a clear prompt to the language model.

2. Vector Database Integration: In this app, we will integrate a vector database to provide better context for the prompt. This will enhance the accuracy and relevance of the model's responses.

3. Function Calls: The third app will leverage function calls to enable ChatGPT to call the functions we provide. This will allow the model to perform specific tasks or retrieve information based on user input.

## Setup for this mini-workshop

We'll need a couple of tools:

- Python version 3.12
- Python package installer, pip
- Pipenv for virtual environments.
  
Pipenv is a tool that helps manage Python packages and virtual environments in a project. It combines the functionality of pip (the package installer) and virtualenv (the virtual environment manager) into a single tool.

Test these tools by checking their version.

If your system doesn't find these tools in your shell:

- Test if you need to add anything to the PATH environment variable.
- If you edit your PATH variable, don't forget to restart your shell.

```sh
python --version
# or
python3 --version

pip --version
# or
pip3 --version

pipenv --version

```

Need to install?

[Install python](https://www.python.org/downloads/)

[Install pip](https://pip.pypa.io/en/stable/installation/)

```sh
pip install --user pipenv
```

## Environment variables

Duplicate the .env.example file and rename the resulting duplicate into ".env".
This new file will have your secrets, use it with caution.

---

IMPORTANT:

- Your OPENAI API Key is a secret. It should never be shared with anyone or uploaded.
- Never upload an API Key to any code repository. Make sure your secrets are stored locally in their own files.
- Secrets should always be in files stated in the .gitignore file.
- CAUTION: If you accidentally add a file with secrets to a commit, secrets are now part of your branch history and available for everyone with access to the repo to see it. You need to remove the file with the secrets from all of the repo versions. (This is a real pain in the behind, it's good practice to just set an .env file from the beginning and add the file to the .gitignore list before committing anything at all)
  
---

After you're done with the .env file, it's time for you to create an OPENAI account.

[OpenAI API platform](https://platform.openai.com/apps)

Check if you're able to create an account. If you're new, they'll give you some free credits to try their API services.

After you created your OPENAI account, you need to go to the "API Keys" option in the left side menu. Create a new secret key BE SURE TO COPY THE API KEY BEFORE YOU CLOSE THE DIALOG BOX and paste it somewhere in your laptop.

After the key is created, insert the key as value of OPENAI_API_KEY in the .env file. Remember, this is a secret. Don't share it with anyone. Make sure you have the .env file added to the .gitignore list.

## Langchain

Langchain is an LLM wrapper, in the sense of being the library we're going to use to abstract the LLMs we want to use.

The promise of Langchain is that we can code our apps to be LLM agnostic.
We then only have to do a simple module for the LLM we want to use and easily replace that module whenever needed.

Next in line we're going to do a simple chat app that you can execute in your shell. Go to the chatapp folder and open the README.md inside of it.
