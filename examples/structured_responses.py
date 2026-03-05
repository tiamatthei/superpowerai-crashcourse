from google.genai import Client
from google.genai.types import (
    FunctionDeclaration,
    GenerateContentConfig,
    Tool,
    Part,
    Content,
    GenerateContentResponse,
)

from pydantic_ai import format_as_xml
import json

from dotenv import load_dotenv
from system_prompt import prompt
from models.clima import Clima
from pydantic import BaseModel

load_dotenv()

client = Client()

class GetTemperatureParams(BaseModel):
    city: str
    scale: str


def get_temperature(city: str, scale: str) -> float:
    """
    Gets the temperature for a given city and scale.

    Args:
        city (str): The name of the city to get the temperature for.
        scale (str): The temperature scale to use ('Celsius', 'Fahrenheit', etc).

    Returns:
        float: The temperature in the requested scale.
    """
    # llamaría a una API de clima para obtener la temperatura
    return 20.0


def get_humidity(city: str) -> int:
    """
    Gets the humidity for a given city.

    Args:
        city (str): The name of the city to get the humidity for.

    Returns:
        int: The humidity in %.
    """
    # llamaría a una API de clima para obtener la humedad
    return 50


def get_wind_speed(city: str) -> float:
    """
    Gets the wind speed for a given city.

    Args:
        city (str): The name of the city to get the wind speed for.

    Returns:
        float: The wind speed in km/h.
    """
    # llamaría a una API de clima para obtener la velocidad del viento
    return 10.0

tools = [
    Tool(function_declarations=[FunctionDeclaration.from_callable(client=client, callable=get_temperature)]),
    Tool(function_declarations=[FunctionDeclaration.from_callable(client=client, callable=get_humidity)]),
    Tool(function_declarations=[FunctionDeclaration.from_callable(client=client, callable=get_wind_speed)]),
]

# La configuración (hiperparametros), herramientas, system_prompt, etc
config = GenerateContentConfig(
    system_instruction=format_as_xml(prompt),
    # response_json_schema=Clima.model_json_schema(),
    # response_mime_type="application/json",
    tools=tools,
)

# Este es el primer contenido (prompt) (input)
user_content = Content(
    role="user",
    parts=[Part.from_text(text="¿Cuál es el clima en Conce?")],
)

# Esta es la llamada a la api (modelo) (input)
response = client.models.generate_content(
    config=config,
    model="gemini-2.5-flash",
    contents=[user_content],
)



def tool_processing(response: GenerateContentResponse) -> list[Part]:
    function_response_parts = []
    for part in response.candidates[0].content.parts:
        if part.function_call:
            print("intentó ejecutar", part.function_call.name)
            print("con los parametros:", part.function_call.args)
            result = None

            if part.function_call.name == "get_temperature":
                city = part.function_call.args["city"]
                scale = part.function_call.args["scale"]
                result = get_temperature(city, scale)

            if part.function_call.name == "get_humidity":
                city = part.function_call.args["city"]
                result = get_humidity(city)

            if part.function_call.name == "get_wind_speed":
                city = part.function_call.args["city"]
                result = get_wind_speed(city)

            # El contenido de la respuesta de la función
            function_response_part = Part.from_function_response(
                name=part.function_call.name,
                response={"result": result},
            )
            # Añadimos el contenido de la respuesta de la función a la lista de contenidos
            function_response_parts.append(function_response_part)

        else:
            print(part.text)
    return function_response_parts

# Este es el contenido final (prompt) (input)
function_response_parts = tool_processing(response)

contents = [
    user_content,
    Content(role="model", parts=response.candidates[0].content.parts),
    Content(role="user", parts=function_response_parts),
]


# Esta es la llamada a la api (modelo) (output)
response2 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=contents,
    config=config,
)

function_response_parts2 = tool_processing(response2)

# add to contents
contents = [
    user_content,
    Content(role="model", parts=response.candidates[0].content.parts),
    Content(role="user", parts=function_response_parts),
    Content(role="model", parts=response2.candidates[0].content.parts),
    Content(role="user", parts=function_response_parts2),
]


response3 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=contents,
    config=config,
)

function_response_parts3 = tool_processing(response3)

contents = [
    user_content,
    Content(role="model", parts=response.candidates[0].content.parts),
    Content(role="user", parts=function_response_parts),
    Content(role="model", parts=response2.candidates[0].content.parts),
    Content(role="user", parts=function_response_parts2),
    Content(role="model", parts=response3.candidates[0].content.parts),
    Content(role="user", parts=function_response_parts3),
]

# El resultado de la llamada a la api (modelo) (output)
print(response3.candidates[0].content.parts)


response4 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=contents,
    config=config,
)

function_response_parts4 = tool_processing(response4)

print(response4.candidates[0].content.parts)







# print("El modelo me ha devuelto esto:")
# part = response.candidates[0].content.parts[0]
# if not part.function_call:
#     print("No function call:", response.text)
# else:
#     function_call = part.function_call
#     print(function_call.model_dump_json())

#     print()
#     print("--------------------------------")
#     fc = function_call.model_dump()
#     args = fc.get("args") or {}
#     parametros = GetTemperatureParams(**args)

#     print("Los parámetros (con los que intentó llamar) son:")
#     print(parametros)

#     print()
#     print("--------------------------------")

#     print("Llamé a la función get_temperature con los parámetros:")
#     temp = get_temperature(parametros)

#     function_response_part = Part.from_function_response(
#         name=fc.get("name"),
#         response={"result": temp},
#     )

#     # Send back: original user + model's function_call + our response
#     contents = [
#         user_content,
#         Content(role="model", parts=[part]),
#         Content(role="user", parts=[function_response_part]),
#     ]
#     response2 = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=contents,
#         config=config,
#     )
#     print("Model's final answer:", response2.text)


# data_as_json = json.loads(response.text)

# clima = Clima(**data_as_json)

# print(clima.model_dump_json())


"""
prompt = {
    "system": {
        "attitude": "Eres un asistente de IA que ayuda a los usuarios a resolver sus problemas.",
        "behavior": {
            "clima": "Si el usuario te pregunta sobre el clima, responde con la temperatura, humedad y velocidad del viento.",
            "temperatura": "Si el usuario te pregunta sobre la temperatura, responde con la temperatura en grados Celsius.",
            "humedad": "Si el usuario te pregunta sobre la humedad, responde con la humedad en %.",
            "viento": "Si el usuario te pregunta sobre la velocidad del viento, responde con la velocidad del viento en km/h.",
        },
        "important_rules": [
            "La idea es poder generar respuestas como si fueras un meteorologo profesional que sale en la tele y tira la talla de vez en cuando, así como el Iván Torres del TVN.",
            "No debes responder preguntas que no sean sobre el clima, temperatura, humedad o velocidad del viento.",
        ],
    }
}
-----
config = GenerateContentConfig(
    response_json_schema=Clima.model_json_schema(),
    response_mime_type="application/json",
)
-----

get_temperature_function = {
    "name": "get_temperature",
    "description": "Obtiene la temperatura de una determinada ciudad, en una determinada escala de medición",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "La ciudad a consultar"},
            "scale": {"type": "string", "description": "La escala de medición"},
        },
        "required": ["city", "scale"],
    },
}


get_humidity_function = {
    "name": "get_humidity",
    "description": "Obtiene la humedad de una determinada ciudad",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "La ciudad a consultar"},
        },
        "required": ["city"],
    },
}

get_wind_speed_function = {
    "name": "get_wind_speed",
    "description": "Obtiene la velocidad del viento de una determinada ciudad",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "La ciudad a consultar"},
        },
        "required": ["city"],
    },
}

-----

prompt = Cual es el clima en concepción en celcius?


"""
