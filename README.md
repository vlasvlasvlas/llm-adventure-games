# llm-adventure-games

<img src="media/image-llm-adventure-games.png" width="500">

El repositorio aloja maquetas disponibles mvp y juegos de aventuras que utilizan modelos LLM como motor de juego, basado en una serie de reglas, personajes, localizaciones y acertijos, dentro de un documento de prompteo.

El repositorio contiene por el momento un juego pero el universo de juegos se irá expandiendo a medida de que se generen nuevos prompteos y formas de juego.

Parte del proyecto es probar librerias para el manejo de modelos LLM, ideas de juegos e interfaces visuales.

## Requerimientos

Si bien se está sumando un servidor para jugar directamente online, por el momento se puede jugar de forma local descargando el repositorio e instalando las dependencias.

- Utiliza Python 3.11+, langchain, gradio y modelos de OpenAI.

- Dependencias en el requirements.txt (openai, langchain, gradio, python-dotenv)

# Juegos 

## Lovecraft LLM: Sombras Insondables.

![Alt text](media/image-lovecraft.png)

Aventura de texto oscura y surrealista, utilizando un modelo LLM de texto generativo, basado en la obra y universo de HP Lovecraft.

- Prompt : https://github.com/vlasvlasvlas/llm-adventure-games/blob/main/prompts/lovecraft_prompt.md
- Cli version : https://github.com/vlasvlasvlas/llm-adventure-games/tree/main/01-lovecraftworld-game-cli
- Web version : https://github.com/vlasvlasvlas/llm-adventure-games/tree/main/01-lovecraftworld-game-web

