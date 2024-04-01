# Chat application

## Objective

We need to chat with our LLM. So a couple of things down our path for the first version of the LLM.

1. Load our .env file.
2. Create an "llms" folder and create a module inside of it called OpenAI.py
3. Configure our LLM with prompt templates.
4. Our app needs to expect our input.
5. The input will be considered a prompt to the LLM.
6. Send the prompt to the LLM and receive its response. Print it.

### Setup

Install app dependencies using pipenv. This will create a file called Pipfile.lock and install the dependencies in a Pipenv isolated environment.

```sh
pipenv install
```

Now you need to start the isolated environment shell for it to load all the necessary libraries installed in the step before.

```sh
pipenv shell
```

Once the shell gets started, you can now execute your python file as you normally would.

```sh
# inside the pipenv shell
python example.py
```

If there's any problem with the installed libraries:

1. exit the pipenv shell with the shell command ```exit```
2. delete the Pipfile.lock from the folder chatapp
3. install the libraries again using ```pipenv install```
4. restart the shell with ```pipenv shell```

Create a **main.py** file inside the chatapp folder. We'll use this file to build our app.

### Load the .env file

Let's just get this out of the way. Assuming you didn't change the folder tree of the repo, load the contents of .env and use the dotenv library to load them.

In the **main.py** file:

```py
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env') 
load_dotenv(dotenv_path)
```

This will load the OPENAI_API_KEY env variable.

### Create a OpenAI LLM python module

1. Next, let's create a folder called "llms", inside of "chatapp" folder.
2. Create files openai.py and \_\_init\_\_.py inside of the "llms" folder.
3. Leave the contents of \_\_init\_\_.py blank.
4. The contents of openai.py will be the following:

```py
from langchain_openai import ChatOpenAI

def build_llm(chat_args):
    return ChatOpenAI() #it automatically looks for the .env API KEY
```

We're done with the openai module.
This way, we keep things separated and we are able to build llms from other companies in the future without changing much of our code.
Note: you noticed there's an empty \_\_init\_\_.py file. The purpose is to let python know all files in the same folder as this file will be treated as packages. [More info](https://discuss.python.org/t/how-exactly-does-init-py-influence-module-search-order/24759)

### Langchain Prompt Templates

Going back to main.py, we're going to use a [Chat Prompt template](https://python.langchain.com/docs/modules/model_io/prompts/quick_start#chatprompttemplate) from Langchain.
[Prompt templates](https://python.langchain.com/docs/modules/model_io/prompts/quick_start) convert raw user input to better input to the LLM.

Import the Chat Prompt Template. The {input} tag is the placeholder tag we'll be using to identify which section will be replaced by our input.

On the import section add:

```py
from langchain_core.prompts import ChatPromptTemplate
```

On the code itself, build your prompt template: 

```py

prompt = ChatPromptTemplate.from_messages([
    #("system", "You are an British gentleman chatter, reply back in cockney style."),
    ("system", "You are math teacher, reply in short sentences. Use math equations whenever possible."),
    ("user", "My message to you: {input}")
])

```

### Langchain Chains

[Chains](https://python.langchain.com/docs/modules/chains) are calls to services (llm services, memory services,) that can be connected like lego pieces. A chain process expects inputs and outputs, and outputs of a chain can be connected as inputs of a second chain in the process.

In this case we're going to use a normal LLMChain from the Langchain's legacy chain set.

On the import section:

```py
from langchain.chains import LLMChain
```

Build your own chain with all the pieces you build before, the LLM and the prompt template.
Use verbose mode to see what's happening behind.

```py
chain = LLMChain(
    llm=chat,
    prompt=prompt,
    verbose=True
)
```

Now let's set up a quick while loop that expects input from the user and inserts it to the prompt template.
Use chain.invoke to send your prompt to the llm. use the key {input} to set up the template.

```py
while True:
    user_input = input(">> ")
    if user_input == "exit":
        break
    response = chain.invoke({'{input}': user_input})
    print("AI:", response)
```

Try it a couple of times. Are you noticing a problem?

Ask the LLM to answer what's 3 + 5. For a second input tell it to add 4 to the previous result. What happens?

### Memory

Our LLM seems to be amnesiac. We need a memory system.

Options:

1. We can keep a log of messages. A message history kept somewhere and sent to the LLM as part of the prompt. (The prompts grow larger and larger as you keep chatting with the LLM)
2. We can use a summary memory system.
    - The summary memory system is designed for an LLM to give us a summary of the last interactions.
    - Our chain becomes designed to send a prompt with the summary and the current question to the LLM.
    - We keep the chat contextualized and the LLM answers correctly.

In the imports part:

```py

from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder #changed line
from langchain.memory import ConversationSummaryMemory #, FileChatMessageHistory #new line
```

Build your memory object, it's important that you set the memory_key the same key you'll use in the prompt object. [More about ConversationSummaryMemory](https://python.langchain.com/docs/modules/memory/types/summary)

```py
memory = ConversationSummaryMemory(
    llm=chat,
    return_messages=True,
    memory_key='summary',
    #chat_memory=FileChatMessageHistory("chat_history.json")
)
```

Change your prompt object to get the summary key information. [More about MessagePlaceholder](https://python.langchain.com/docs/modules/model_io/concepts#messagesplaceholder). [More about HumanMessagePromptTemplate](https://python.langchain.com/docs/modules/model_io/concepts#messageprompttemplate)

```py
prompt = ChatPromptTemplate(
    input_variables=["input"],
    messages=[ 
        MessagesPlaceholder(variable_name="summary"),
        HumanMessagePromptTemplate.from_template("{input}")
    ]
)
```

Now we change the chain object to include our memory object.

```py
chain = LLMChain(
    llm=chat,
    prompt=prompt,
    memory=memory,
    verbose=True
)
```

Finally edit the While loop to just print the output key (we didn't change the key so it should be 'text')

```py
while True:
    user_input = input(">> ")
    if user_input == "exit":
        break
    response = chain.invoke({user_input})
    print("AI:", response['text'])
```

Let's try again.

1. Ask LLM what 3+5 is. Then ask what happens if you add 4 to the previous answer.
What happened?

You should have good answers from the LLM. 

Exercise: Uncomment the `FileChatMessageHistory` import and change `ConversationSummaryMemory` to `ConversationBufferMemory` and see how it behaves different.
Open the app, try some tabs. Close the app, then open again and try to continue your previous chat. What's happening?

Now your messages are being stored on chat_history.json, because when you built the memory object, you set it up to store the messages with the chat_memory key.

Onto the next part. Go to the folder facts and we'll learn about embeddings. Open the README.md file over there.
