"""
import gradio as gr

def greet(name, is_morning, temperature):


    salutation = "Good morning" if is_morning else "Good evening"
    greeting = f"{salutation} {name}. It is {temperature} degrees today"
    celsius = (temperature - 32) * 5 / 9
    
    
    # 2 returns: text and number
    return greeting, round(celsius, 2)

demo = gr.Interface(

    title="Testo",
    description="Desc testo Lorem Ipsum",
    article="Bottom Articolo testo Lorem Ipsum",
    allow_flagging=False,

    fn=greet,

    
    inputs=["text", "checkbox", gr.Slider(0, 100)],

    # expected outputs
    outputs=["text", "number"],
)
demo.launch()
"""

"""
import random
import gradio as gr

def random_response(message, history):
    return random.choice(["Yes", "No"])

demo = gr.ChatInterface(random_response)

demo.launch()
"""

"""
import gradio as gr


def greet(name):
    return "Hello " + name + "!"


with gr.Blocks() as demo:

    name = gr.Textbox(label="Name")
    output = gr.Textbox(label="Output Box")
    greet_btn = gr.Button("Greet")

    greet_btn.click(fn=greet, inputs=name, outputs=output, api_name="APIgreet")

demo.launch()
"""

import numpy as np
import gradio as gr


def flip_text(x):
    return x[::-1]


def flip_image(x):
    return np.fliplr(x)


with gr.Blocks() as demo:
    gr.Markdown("Flip text or image files using this demo.")
    with gr.Tab("Flip Text"):
        text_input = gr.Textbox()
        text_output = gr.Textbox()
        text_button = gr.Button("Flip")
    with gr.Tab("Flip Image"):
        with gr.Row():
            image_input = gr.Image()
            image_output = gr.Image()
        image_button = gr.Button("Flip")

    with gr.Accordion(label="Open for More!",open=False):
        gr.Markdown("### Look at me...")

    text_button.click(flip_text, inputs=text_input, outputs=text_output)
    image_button.click(flip_image, inputs=image_input, outputs=image_output)

demo.launch()
