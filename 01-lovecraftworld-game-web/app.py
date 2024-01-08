# Set env var OPENAI_API_KEY or load from a .env file:
import os, sys
from dotenv import load_dotenv, find_dotenv

load_dotenv(override=True)

from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage,AIMessage, HumanMessage,ChatMessage
import gradio as gr

# Prompt
prompt_md = os.environ.get("LOVECRAFT_PROMPT_MD")

md_title = """
    # {title}
    ## {subtitle}
    🎵 🎧 Te recomiendo abrir el siguiente [link de audio]({music}&target=_blank) para escuchar mientras juegas.. 
    """.format(
    title=os.environ.get("LOVECRAFT_TITLE"),
    subtitle=os.environ.get("LOVECRAFT_SUBTITLE"),
    music=os.environ.get("LOVECRAFT_MUSIC"),
)

with open(prompt_md, encoding="utf-8") as fh:
    extprompt = fh.read()

dataprompt = """
            El siguiente texto en formato markdown es toda la información que debes respetar y utilizar para darle forma al juego.
            CONTEXT START: inicio del markdown --> 

            {extprompt}

            <-- fin del markdown. CONTEXT END.
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

    print("message: ", message)

    """
    if len(history) > 1:
        print("history: ", history)        
        for human, ai in history:
            history_langchain_format.append(HumanMessage(content=human))
            history_langchain_format.append(AIMessage(content=ai))
    """

    history_langchain_format.append(SystemMessage(content=dataprompt))
    history_langchain_format.append(AIMessage(content=history))
    history_langchain_format.append(HumanMessage(content=message))

    print("history_langchain_format: ", history_langchain_format)

    gpt_response = llm(history_langchain_format)

    # carga a output historico
    existing_text = output_hist.value

    # Actualizar el historial del chat
    output_hist.value = (
        existing_text
        + "\n\n ` " + message + " `"
        + "\n\n " + gpt_response.content
    )

    return output_hist.value


# gradio blocks gui
with gr.Blocks(
    title=os.environ.get("LOVECRAFT_TITLE"),
    theme=gr.Theme.from_hub("Taithrah/Minimal"),
) as demo:
    # Titulo y desc
    gr.Markdown(md_title)

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
    output_hist = gr.Markdown(show_label=False)

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

    # enviar: onclick
    btnSnd.click(fn=predict, inputs=[textbox,output_hist], outputs=output_hist)
    # enviar: al presionar enter
    textbox.submit(fn=predict, inputs=[textbox,output_hist], outputs=output_hist)

    # clean input
    btnSnd.click(lambda x: gr.update(value=""), [], [textbox])
    textbox.submit(lambda x: gr.update(value=""), [], [textbox])

    # launch
    demo.launch(
        share=True
        #,auth=("chirim", "bolito"),  # remove this line to disable authentication
    )
