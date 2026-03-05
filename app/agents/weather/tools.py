from weather.models import (
    GetTemperatureParams,
    GetHumidityParams,
    GetWindSpeedParams,
    TemperatureOutput,
    HumidityOutput,
    WindSpeedOutput,
)
from pydantic_ai import FunctionToolset, Tool


async def get_temperature(params: GetTemperatureParams) -> TemperatureOutput:
    """
    Obtiene la temperatura de una determinada ciudad,
    en una determinada escala de medición
    """
    return 20.0


async def get_humidity(params: GetHumidityParams) -> HumidityOutput:
    """
    Obtiene la humedad de una determinada ciudad
    """
    return 50


async def get_wind_speed(params: GetWindSpeedParams) -> WindSpeedOutput:
    """
    Obtiene la velocidad del viento de una determinada ciudad
    """
    return 10.0


weather_tools = FunctionToolset(
    [
        Tool(get_temperature, name="get_temperature"),
        Tool(get_humidity, name="get_humidity"),
        Tool(get_wind_speed, name="get_wind_speed"),
    ]
)
