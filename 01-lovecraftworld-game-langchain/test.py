# Set env var OPENAI_API_KEY or load from a .env file:
import os, sys
from dotenv import load_dotenv, find_dotenv

load_dotenv(override=True)
print("key check:", os.environ.get("OPENAI_API_KEY"))


prompt_json = 'promptutf8.json'

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
"""

"""
import json
from pathlib import Path
from pprint import pprint


file_path='prompt.json'

with open(file_path, encoding='utf-8') as fh:
    data = json.load(fh)

print(data)

# Ruta al archivo JSON que quieres guardar
archivo_salida = 'promptutf8.json'

# Guardar el archivo JSON con la codificación UTF-8
with open(archivo_salida, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)


with open(archivo_salida, encoding='utf-8') as fh:
    datautf8 = json.load(fh)

print(datautf8)


#Loader that loads data from JSON.
import json
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader


class JSONLoader(BaseLoader):
    def __init__(
        self,
        file_path: Union[str, Path],
        content_key: Optional[str] = None,
        ):
        self.file_path = Path(file_path).resolve()
        self._content_key = content_key
        
    def load(self) -> List[Document]:
        #Load and return documents from the JSON file.

        docs=[]
        # Load JSON file
        with open(self.file_path) as file:
            data = json.load(file)

            # Iterate through 'pages'
            for page in data['pages']:
                parenturl = page['parenturl']
                pagetitle = page['pagetitle']
                indexeddate = page['indexeddate']
                snippets = page['snippets']

                # Process snippets for each page
                for snippet in snippets:
                    index = snippet['index']
                    childurl = snippet['childurl']
                    text = snippet['text']
                    metadata = dict(
                        source=childurl,
                        title=pagetitle)

                    docs.append(Document(page_content=text, metadata=metadata))
        return docs


from langchain_community.document_loaders import JSONLoader

loader = JSONLoader(
    file_path=archivo_salida,
    #jq_schema='.content',
    #text_content=False,
    json_lines=False
    )

print(loader)

data = loader.load()


#from langchain.indexes import VectorstoreIndexCreator

#index = VectorstoreIndexCreator().from_loaders([loader])
""" 



from langchain_community.document_loaders import TextLoader

loader = TextLoader(prompt_json)

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(texts, embeddings)


retriever = db.as_retriever(search_kwargs={"k": 1})

print(retriever.get_relevant_documents("que empieze el juego"))
