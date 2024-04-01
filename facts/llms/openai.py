
from langchain_openai import ChatOpenAI

def build_llm(chat_args):
    return ChatOpenAI(
        #callbacks=chat_args["callbacks"]
    )