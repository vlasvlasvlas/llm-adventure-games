# Set env var OPENAI_API_KEY or load from a .env file:
import os, sys
from dotenv import load_dotenv, find_dotenv

load_dotenv(override=True)

from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
import gradio as gr

# Prompt
prompt_md = os.environ.get("PROMPT_MD")

with open(prompt_md, encoding="utf-8") as fh:
    extprompt = fh.read()

dataprompt = """
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
            - Respeta el MARKDOEN de contexto como la biblia del juego, tanto los personajes acertijos localizaciones y reglas de oro del juego.
            - El juego debe tener un final claro luego de finaliar todos los acertijos de todas las localizaciones.
            """.format(
    extprompt=extprompt
)

# OpenAI API Key
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

# langchain llm
llm = ChatOpenAI(
    model_name=os.environ.get("LLM_NAME"), temperature=os.environ.get("LLM_TEMPERATURE")
)

# Initialize history outside of the predict function
history_langchain_format = []


# langchain predict function
def predict(message, history=None):
    if history is not None:
        for human, ai in history:
            history_langchain_format.append(HumanMessage(content=human))
            history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=message))

    custom_prompt = dataprompt
    history_langchain_format.append(HumanMessage(content=custom_prompt))
    gpt_response = llm(history_langchain_format)

    # Agregar el nuevo mensaje al final del texto existente

    # carga a output historico
    existing_text = output_hist.value

    # Actualizar el historial del chat
    output_hist.value = (
        existing_text
        + "\n\n\n > **Jugador**: "
        + message
        + "\n\n > **Historia**: "
        + gpt_response.content
    )

    return output_hist.value


# gradio blocks gui
with gr.Blocks(
    title="Sombras Insondables - Lovecraft LLM",
    theme=gr.Theme.from_hub("Taithrah/Minimal"),
) as demo:
    # Titulo y desc
    gr.Markdown(
        """
                # Sombras Insondables - Lovecraft LLM
                ## Aventura de texto oscura y surrealista, utilizando un modelo LLM de texto generativo, basado en la obra y universo de HP Lovecraft.
                """
    )

    with gr.Accordion("Acciones del juego"):
        with gr.Row():
            # Ejemplos
            btn1 = gr.Button("Que empieze el juego!", size="sm")
            btn2 = gr.Button("Que reinicie el juego!", size="sm")
            btn3 = gr.Button("Que termine el juego!", size="sm")

    # titul acciones del juego
    gr.Markdown(
        """
                Historia:
                """
    )

    # texto output hist
    output_hist = gr.Markdown(show_label=True)

    # texto input
    textbox = gr.Textbox(
        placeholder="Escribe aquí tu mensaje", container=False, autofocus=True, scale=8
    )

    # btn enviar
    btnSnd = gr.Button("Enviar")

    # acciones
    btn1.click(fn=lambda: "Que empieze el juego!", outputs=textbox)
    btn2.click(fn=lambda: "Que reinicie el juego!", outputs=textbox)
    btn3.click(fn=lambda: "Que termine el juego!", outputs=textbox)

    # enviar onclick
    btnSnd.click(fn=predict, inputs=textbox, outputs=output_hist)
    # enviar al presionar enter
    textbox.submit(fn=predict, inputs=textbox, outputs=output_hist)
    textbox.submit(lambda x: gr.update(value=""), [], [textbox])

    # launch
    demo.launch(share=True)
