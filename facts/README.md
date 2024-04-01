# facts application

## Objective

We have a list of facts we want to ask our LLM about. We don't want the LLM to get out of the list scope.

We have 2 options:

1. Provide the whole 500 facts inside our `facts.txt`. Everytime you prompt your LLM to answer something from the facts file, it will process all of its tokens and you'll be charged for it every time you need an answer for your prompt.
2. Section your document into a number of chunks. Build a system that finds similarities between your prompt and the most relevant chunks of `facts.txt`. Attach the most relevant chunk or chunks to the prompt and send it to the LLM. This way you won't process the whole document everytime, just the most relevant chunk.

This is cute and all, but how will we build such a system that find similarities?

Lucky for you, the system is already built and you just have to import it.
What we want is a vector database. Something we can query two strings by similarity scores and retrieve results by similarity.

## Some steps to take

1. Load our .env file.
2. Create an "llms" folder and create a module inside of it called OpenAI.py
3. Create a vector database resorting to sqlite.
4. Create embeddings from our file facts.txt
5. Configure our LLM to query for relevant embeddings.
6. Our app needs to expect our input and the relevant section.
7. Send the prompt to the LLM and receive its response. Print it.

In our use case, we want to create embeddings from the document `facts.txt`.
We'll do this in a separate file called `create_embeddings.py`.

## Plan of action for create_embeddings.py

1. Divide our document into chunks of a certain size.
2. Let OpenAI calculate embeddings for each chunk using its training data.
3. We then store the calculated embeddings together with the chunk in our database
4. Everytime we send a prompt to the LLM, we search for a similar chunk in our database and send it together with our prompt. Our LLM will receive context and will answer accordingly.

NOTE: everytime you ask OpenAI to create embeddings, you'll spend tokens to do this action.
Plan your app to not create embeddings everytime it runs, just run them once and if everything is okay, you'll have an embedding system ready to be used for the subsequent runs.

## Setting up environment variables

Create a `create_embeddings.py` file inside facts folder import a couple of things to load environment variables.

Verify you have the folder `llms` present with the openai.py file inside.

```py
from os.path import join, dirname
from dotenv import load_dotenv
from llms.openai import build_llm
```

## Cutting our document in chunks

Langchain provides us with a couple of tools we're going to need.
A document loader and a text splitter.

```py
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
```

## Embeddings

Embeddings are a way of representing categorical data, like words, by mapping them to vectors of continuous numbers. They are used to capture the semantic context and relationships between words. For example, words that are used in similar contexts, like "dog" and "puppy", will have similar vectors.

```py
from langchain_openai import OpenAIEmbeddings
```

## Vector Stores

Vector Stores store our embeddings in databases. Our database will contain the vector values.
We're going to use chromadb to store information inside a sqlite file.
[More info about vector stores](https://python.langchain.com/docs/modules/data_connection/vectorstores/)

```py
from langchain_community.vectorstores import Chroma
```

## Initiate OpenAI Embeddings Object

```py
embeddings = OpenAIEmbeddings()
```

## Dividing our document into chunks

Initiate a splitter that separates chunks by `\n` (new line character).
Make chunks have circa 200 characters, but don't let this number size cut lines in the middle.
Luckily, splitters will always use the separator character to cut the chunks needed.
We can overlap the chunks by 50 characters.

Overlapping chunks offer you a smooth transition between chunks of a document. This can be relevant for documents that talk extensively about a certain subject.

For all these aspects you have `CharacterTextSplitter` with `separator`, `chunk_size` and `chunk_overlap`. Add the following code to your `create_embeddings.py` file and try to understand what it does.

```py
textSplitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=200,
    chunk_overlap=50
)

loader = TextLoader("facts.txt")
split_doc = loader.load_and_split(textSplitter)
```

## Create our embeddings database from our split documents

Now we need to create our vector database by using Chroma.
Chroma will take each chunk, ask OpenAI's model to create embeddings using its training data for that chunk and store the chunk + chunk's embeddings into our database.

```py
db = Chroma.from_documents(
    split_doc, 
    embedding=embeddings,
    persist_directory="embeddings"
)
```

The `embedding` property takes your OpenAIEmbeddings engine you set before. `Persist_directory` property indicates you which folder to store this database. If folder doesn't exist, it will create the folder for you.

## Run create_embeddings.py

Don't forget to do the pipenv procedure to create an environment.

```sh
pipenv install #if you didn't install the dependencies noted inside Pipfile
pipenv shell
```

After shell is initialized:

```sh
python create_embeddings.py
```

## Query our vector database for embeddings

We created our db object and now we are ready to query it.
So let's test it out.

Create a new file called `test_embeddings`.

There are a couple of queries by similarity you can do. [More info about search queries by similarity](https://python.langchain.com/docs/modules/data_connection/vectorstores/#similarity-search-1)

```py
#test_embeddings
from langchain_openai import OpenAIEmbeddings
from os.path import join, dirname
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma

dotenv_path = join(dirname(__file__), '..' , '.env')
load_dotenv(dotenv_path)

embeddings = OpenAIEmbeddings()

# load our Chroma vector database with OpenAIEmbeddings
# refer to persisted data from the folder embeddings
db = Chroma(
    embedding_function=embeddings, 
    persist_directory="embeddings"
)

results = db.similarity_search_with_score(
    "Tell me a fact about possums.",
    k=4)

# results = db.similarity_search( "Tell me a fact about cats.", k=6)

for result in results:
    print("\n")
    print(result)
```

Did it work well? What was printed? Discuss what happened.

## Now for the main masterpiece

Create a file named `main.py`.

1. Again, make sure you have the necessary code to load environment variables.
2. We know how to load our chroma database to find relevant chunks for our prompts.

```py

from os.path import join, dirname
from dotenv import load_dotenv
from llms.openai import build_llm
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
#imports are missing here, oopsiedaisy

```

And for what we already know:

1. Load env vars
2. build llm
3. initiate OpenAIEmbeddings
4. initiate Chroma DB

```py
dotenv_path = join(dirname(__file__), '..' , '.env')
load_dotenv(dotenv_path)

llm = build_llm({})

embeddings = OpenAIEmbeddings()

db = Chroma(
    embedding_function=embeddings, 
    persist_directory="emb"
)
```

What's left is to build our LLM chain and connect a prompt template to it, using our own prompt and the relevant chunks we find.

## Retrievers

We could write the rest of the code and design the prompt ourselves, but where's the fun in that?

Fortunately for you, there's a thing called `Retrievers`.
These peeps are here to help you retrieve data from the database and connect it to our LLM chain.
[More info on Retrievers](https://python.langchain.com/docs/modules/data_connection/retrievers/)

```py
retriever = db.as_retriever()
```

Then refer the retriever to our chain we're about to built.
We're going to need a RetrievalQA chain so don't forget to import it.
Check about RetrievalQA on the above link.

```py
chain = RetrievalQA.from_chain_type(
    'retriever'=retriever,
    'llm'=llm
)

chain.invoke({"Tell me a fact about possums."})
```

Then on the pipenv shell terminal, run `python main.py` and check the result.

## What is exactly happening?

You saw that the LLM is telling you a fact about the information you have in facts.txt.
You've seen how we can check for document chunks that can be related to your prompt by similarity.

But what's happening behind the scenes?

We're going to use a tool already included in the "handlers" folder.
This tool is going to be used by our llm on its callback properties.
[More about callbacks](https://python.langchain.com/docs/modules/callbacks/)

On main.py, import the handler

```py
from handlers.chat_model_start_handler import ChatModelStartHandler
```

If you check the code on this handler, you'll see it's a class extended from BaseCallbackHandler from Langchain.callbacks

It overrides the function on_chat_model_start and lets us see the content of prompts.

Change the build_llm function to include the callback and run the file again.

```py
llm = build_llm({
    "callbacks": [ChatModelStartHandler()]
})
```
