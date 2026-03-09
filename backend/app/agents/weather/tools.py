from app.agents.weather.models import (
    GetTemperatureParams,
    GetHumidityParams,
    GetWindSpeedParams,
    TemperatureOutput,
    HumidityOutput,
    WindSpeedOutput,
)
from pydantic_ai import FunctionToolset, Tool


import asyncio

async def get_temperature(params: GetTemperatureParams) -> TemperatureOutput:
    """
    Obtiene la temperatura de una determinada ciudad,
    en una determinada escala de medición
    """
    await asyncio.sleep(3)  # Simular delay de 1 segundo
    return TemperatureOutput(
        current_temperature=20.0,
        max_temperature=25.0,
        min_temperature=18.0,
        mean_temperature=20.5,
    )

async def get_humidity(params: GetHumidityParams) -> HumidityOutput:
    """
    Obtiene la humedad de una determinada ciudad
    """
    await asyncio.sleep(3)  # Simular delay de 1 segundo
    return HumidityOutput(
        current_humidity=50,
        max_humidity=60,
        min_humidity=40,
        mean_humidity=50
    )

async def get_wind_speed(params: GetWindSpeedParams) -> WindSpeedOutput:
    """
    Obtiene la velocidad del viento de una determinada ciudad
    """
    await asyncio.sleep(3)  # Simular delay de 1 segundo
    return WindSpeedOutput(
        current_wind_speed=10.0,
        max_wind_speed=15.0,
        min_wind_speed=5.0,
        mean_wind_speed=10.0
    )


weather_tools = FunctionToolset(
    [
        Tool(get_temperature, name="get_temperature"),
        Tool(get_humidity, name="get_humidity"),
        Tool(get_wind_speed, name="get_wind_speed"),
    ]
)
