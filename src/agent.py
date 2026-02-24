import os
from dotenv import load_dotenv

load_dotenv()
if not os.environ.get("GOOGLE_API_KEY") and os.environ.get("GEMINI_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

from pydantic_ai import format_as_xml, Agent
from pydantic import Field, BaseModel
from src.system_prompt import prompt
from src.models import GetTemperatureParams, GetHumidityParams, GetWindSpeedParams



class IvanTorresOutput(BaseModel):
    title: str = Field(description="El titulo de la respuesta")
    description: str = Field(description="La descripción de la respuesta")
    tools: list[str] = Field(description="Las herramientas que se han utilizado")


ivan_torres = Agent("google-gla:gemini-2.5-flash")

ivan_torres.instrument_all()



@ivan_torres.tool_plain
async def get_temperature(params: GetTemperatureParams) -> float:
    """
    Obtiene la temperatura de una determinada ciudad,
    en una determinada escala de medición
    """
    return 20.0


@ivan_torres.tool_plain
async def get_humidity(params: GetHumidityParams) -> int:
    """
    Obtiene la humedad de una determinada ciudad
    """
    return 50


@ivan_torres.tool_plain
async def get_wind_speed(params: GetWindSpeedParams) -> float:
    """
    Obtiene la velocidad del viento de una determinada ciudad
    """
    return 10.0


@ivan_torres.system_prompt
def system_prompt():
    return format_as_xml(prompt)
