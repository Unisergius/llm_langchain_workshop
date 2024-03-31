from os.path import join, dirname
from dotenv import load_dotenv
from llms.openai import build_llm
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationSummaryMemory, FileChatMessageHistory
from langchain.chains import LLMChain, SequentialChain


dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

chat = build_llm({})

cockney_prompt = ChatPromptTemplate(
    input_variables=["input"],
    messages=[ 
        SystemMessagePromptTemplate.from_template(
            "You are an British gentleman chatter, reply back in cockney style."
        ),
        MessagesPlaceholder(variable_name="summary"),
        HumanMessagePromptTemplate.from_template("{input}")
    ],
)

translator_prompt = ChatPromptTemplate(
    input_variables=["cockney_output", "input"],
    messages=[ 
        SystemMessagePromptTemplate.from_template(
            "Translate the following sentence from cockney slang to normal english."
        ),
        HumanMessagePromptTemplate.from_template("{cockney_output}")
    ]
)

memory = ConversationSummaryMemory(
    llm=chat,
    return_messages=True,
    memory_key='summary',
    chat_memory=FileChatMessageHistory("messages.json"),
    input_key="input"
)

cockney_chain = LLMChain(
    llm=chat,
    prompt=cockney_prompt,
    memory=memory,
    verbose=True,
    output_key="cockney_output"
)

translator_chain = LLMChain(
    llm=chat,
    prompt=translator_prompt,
    memory=memory,
    verbose=True,
    output_key="translated_output"
)

chain = SequentialChain(
    chains=[
        cockney_chain, 
        translator_chain
    ],
    input_variables=["input"],
    output_variables=["cockney_output", "translated_output"]
)

while True:
    user_input = input("\n>> ")
    if user_input == "exit":
        break
    response = chain.invoke({"input": user_input})
    print("\n[Human AI]:\n", user_input)
    print("\n[Cockney AI]:\n", response['cockney_output'])
    print("\n[Translated AI]:\n", response['translated_output'])