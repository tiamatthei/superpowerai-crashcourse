from pydantic import BaseModel, Field


class IvanTorresOutput(BaseModel):
    title: str = Field(description="El titulo de la respuesta")
    description: str = Field(description="La descripción de la respuesta")
    tools: list[str] = Field(description="Las herramientas que se han utilizado")


class GetTemperatureParams(BaseModel):
    city: str = Field(description="La ciudad a consultar")
    scale: str = Field(default="celsius", description="La escala de medición")


class GetHumidityParams(BaseModel):
    city: str = Field(description="La ciudad a consultar")


class GetWindSpeedParams(BaseModel):
    city: str = Field(description="La ciudad a consultar")


class TemperatureOutput(BaseModel):
    current_temperature: float = Field(description="La temperatura actual en grados Celsius")
    max_temperature: float = Field(description="La temperatura máxima en grados Celsius")
    min_temperature: float = Field(description="La temperatura mínima en grados Celsius")
    mean_temperature: float = Field(description="La temperatura media en grados Celsius")


class HumidityOutput(BaseModel):
    current_humidity: int = Field(description="La humedad actual en %")
    max_humidity: int = Field(description="La humedad máxima en %")
    min_humidity: int = Field(description="La humedad mínima en %")
    mean_humidity: int = Field(description="La humedad media en %")


class WindSpeedOutput(BaseModel):
    current_wind_speed: float = Field(description="La velocidad del viento en km/h")
    max_wind_speed: float = Field(description="La velocidad del viento máxima en km/h")
    min_wind_speed: float = Field(description="La velocidad del viento mínima en km/h")
    mean_wind_speed: float = Field(description="La velocidad del viento media en km/h")