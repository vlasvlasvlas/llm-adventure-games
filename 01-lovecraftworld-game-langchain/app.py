# Set env var OPENAI_API_KEY or load from a .env file:
import os, sys
from dotenv import load_dotenv, find_dotenv

load_dotenv(override=True)
print("key check:", os.environ.get("OPENAI_API_KEY"))

""" 
# test 
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import OpenAI

from langchain.chains import ConversationChain

from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferWindowMemory


# It creates a summary of the conversation over time.
# This memory is most useful for longer conversations where the full message history would consume many tokens.
from langchain.memory import ConversationSummaryMemory

# It uses token length rather than number of interactions to determine when to flush interactions.
from langchain.memory import ConversationSummaryBufferMemory

llm = OpenAI(temperature=0)

memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=10)

memory.save_context({"input": "hi"}, {"output": "whats up"})
memory.save_context(
    {"input": "im working on better docs for chatbots"},
    {"output": "oh, that sounds like a lot of work"},
)
memory.save_context(
    {"input": "yes, but it's worth the effort"},
    {"output": "agreed, good docs are important!"},
)

print(memory.load_memory_variables({}))

"""


from langchain.chains import ConversationChain

from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferWindowMemory

from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import OpenAI

from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

# LLM
llm = ChatOpenAI()

# Prompt
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "You are a nice chatbot having a conversation with a human."
        ),
        # The `variable_name` here is what must align with memory
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
)

# Notice that we `return_messages=True` to fit into the MessagesPlaceholder
# Notice that `"chat_history"` aligns with the MessagesPlaceholder name
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation = LLMChain(llm=llm, prompt=prompt, verbose=True, memory=memory)

# Notice that we just pass in the `question` variables - `chat_history` gets populated by memory
conversation({"question": "hi"})

conversation(
    {"question": "Translate this sentence from English to French: I love programming."}
)

conversation({"question": "Now to spanish."})

print(conversation)