# Set env var OPENAI_API_KEY or load from a .env file:
import os, sys
from dotenv import load_dotenv, find_dotenv
load_dotenv(override=True)

from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
import gradio as gr

# Prompt
prompt_md = os.environ.get("PROMPT_MD")

with open(prompt_md, encoding='utf-8') as fh:
    extprompt = fh.read()

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
    
# OpenAI API Key
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

# langchain llm
llm = ChatOpenAI(
    model_name=os.environ.get("LLM_NAME"), 
    temperature=os.environ.get("LLM_TEMPERATURE")
    )

# Initialize history outside of the predict function
history_langchain_format = []

# langchain predict function
def predict(message, history):

    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=message))
    
    custom_prompt = dataprompt 
    history_langchain_format.append(HumanMessage(content=custom_prompt))
    
    gpt_response = llm(history_langchain_format)
    return gpt_response.content

# gradio chat gui
demo = gr.ChatInterface(
    fn=predict,
    title="Sombras Insondables - Lovecraft LLM",
    description="Aventura de texto oscura y surrealista, utilizando un modelo LLM de texto generativo, basado en la obra y universo de HP Lovecraft.",
    theme=gr.Theme.from_hub('Taithrah/Minimal'),
    textbox=gr.Textbox(placeholder="Escribe aquí tu mensaje", container=False, scale=8),
    submit_btn="Enviar",
    stop_btn=None,
    undo_btn=None,
    retry_btn=None,
    clear_btn=None,
    examples=["Que empieze el juego!", "Que reinicie el juego!", "Que termine el juego!"],
    examples_label="Acciones del juego"
)

# gradio launch
demo.launch(share=True)
