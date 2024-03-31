from langchain.callbacks.base import BaseCallbackHandler
from pyboxen import boxen

def boxen_print(*args, **kwargs):
    print(boxen(*args, **kwargs))
    

class ChatModelStartHandler(BaseCallbackHandler):
    def on_chat_model_start(self, serialized, messages, **kwargs):
        print("\n\n ========= Sending Messages ========= \n\n")
        for message in messages[0]: 
            color = "grey"
            do_print = True
            if message.type == "system":
                color = "yellow"
            elif message.type == "human":
                color = "green"
            elif message.type == "ai" and "function_call" in message.additional_kwargs:
                call = message.additional_kwargs["function_call"]
                color = "cyan"
                do_print = False
                boxen_print(f"Running tool {call['name']} with args {call['arguments']}", title=message.type, color="cyan")
            elif message.type == "ai":
                color = "blue"
            elif message.type == "function":
                color = "purple"
            if do_print:
                boxen_print(message.content, title=message.type, color=color)