from pydantic import BaseModel, Field
from google.genai import Client
from google.genai.types import GenerateContentConfig

from pydantic_ai import format_as_xml
import json

from dotenv import load_dotenv
from system_prompt import prompt
load_dotenv()

class Clima(BaseModel):
    temperatura: float = Field(
        default=20.0, description="La temperatura en grados Celsius",
        ge=0, le=100
    )
    humedad: int = Field(default=50, description="La humedad en %")
    viento: float = Field(default=10.0, description="La velocidad del viento en km/h")
    una_tallita_pa_distender: str = Field(default="", description="Una tallita pa distender, que siga las reglas de la tele")

# print(Clima(temperatura=60).model_json_schema())

client = Client()


config = GenerateContentConfig(
    system_instruction=format_as_xml(prompt),
    response_json_schema=Clima.model_json_schema(),
    response_mime_type="application/json",
)


response = client.models.generate_content(
    config=config,
    model="gemini-2.5-flash",
    contents="¿Cuál es la temperatura en Conce?",
)

data_as_json = json.loads(response.text)

clima = Clima(**data_as_json)

print(clima.temperatura)
print(clima.humedad)
print(clima.viento)
print(clima.una_tallita_pa_distender)


# print(Clima(temperatura="ase calor", humedad="tropiconce", viento="Caleta").model_dump_json())


