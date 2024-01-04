# Set env var OPENAI_API_KEY or load from a .env file:
import os, sys
from dotenv import load_dotenv, find_dotenv
load_dotenv(override=True)

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

prompt_md = os.environ.get("PROMPT_MD")

# lee prompt externo 
with open(prompt_md, encoding='utf-8') as fh:
    extprompt = fh.read()

# prompt : 
dataprompt = '''
            Tienes que respetar y entender en su totalidad el siguiente texto, sin poder hacer nada contrario al siguiente contenido MARKDOWN:

            CONTEXT START: inicio del markdown --> 

            {extprompt}

            <-- fin del markdown. CONTEXT END.

            Eres el mejor diseñador y motor de juegos de aventura y debes iniciar el juego ya. el texto enviado no debe ser transmitido al jugador, es información que tienes que utilizar para darle forma al juego y solo debes empezar preguntando el nombre al jugador, tal cual lo dicen las reglas de oro. 
            
            Recuerda: 
            - Inicia con la descripcion, escribe parrafos normales sin decir palabras como 'inicio de juego', esto tiene que empezar de forma coloquial como un juego de aventura.
            - Inicias preguntandole el nombre al jugador y con esa respuesta ya debes usarlo dentro del nombre del personaje tipo protagonista. 
            - Nunca debes responder por el jugador y siempre debes esperar a que el jugador responda para seguir. 
            - El jugador puede decidir qué hacer y debes ayudarlo cuando sea necesario con preguntas multiple choice, pero el jugador tambien puede escribir sin usar ninguna de las opciones y el jugador debe saberlo. 
            - Respeta el JSON como la biblia del juego, tanto los personajes acertijos localizaciones y reglas de oro del juego.
            - El juego debe tener un final claro luego de finaliar todos los acertijos de todas las localizaciones.
            '''.format(extprompt=extprompt)


# LLM
llm = ChatOpenAI(
    model_name=os.environ.get("LLM_NAME"), 
    temperature=os.environ.get("LLM_TEMPERATURE")
    )

# Prompt
prompt = ChatPromptTemplate(
    
    # custom system message
    messages=[

        SystemMessagePromptTemplate.from_template(dataprompt),

        # The `variable_name` here is what must align with memory
        MessagesPlaceholder(variable_name="chat_history"),

        HumanMessagePromptTemplate.from_template("{question}"),
    ]
)

# Notice that we `return_messages=True` to fit into the MessagesPlaceholder
# Notice that `"chat_history"` aligns with the MessagesPlaceholder name
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation = LLMChain(llm=llm, prompt=prompt, verbose=False, memory=memory)

def askconv (preg):

    # Notice that we just pass in the `question` variables - `chat_history` gets populated by memory
    conversation({"question": preg})

    convlist = [conversation.memory.chat_memory][0].messages[-1].content

    print("\n\n")
    print(convlist)
    print("\n\n")

def obtener_respuesta(input_usuario):
    askconv(input_usuario)


# Inicio de juego
askconv('Que comienze el juego!')


while True:
    input_usuario = input(" -> ")

    # Verificar si el usuario quiere salir
    if input_usuario.lower() == 'finjuego':
        print("Saliendo del programa.")
        break

    resultado = obtener_respuesta(input_usuario)
