from pydantic import BaseModel, Field


class GetTemperatureParams(BaseModel):
    city: str = Field(default="Concepción", description="La ciudad a consultar")
    scale: str = Field(default="Celsius", description="La escala de medición")


class GetHumidityParams(BaseModel):
    city: str = Field(default="Concepción", description="La ciudad a consultar")


class GetWindSpeedParams(BaseModel):
    city: str = Field(default="Concepción", description="La ciudad a consultar")
