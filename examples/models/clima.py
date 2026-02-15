from pydantic import BaseModel, Field


class Clima(BaseModel):
    temperatura: float = Field(
        default=20.0, description="La temperatura en grados Celsius", ge=0, le=100
    )
    humedad: int = Field(default=50, description="La humedad en %")
    viento: float = Field(default=10.0, description="La velocidad del viento en km/h")
    una_tallita_pa_distender: str = Field(
        default="",
        description="Una tallita pa distender, que siga las reglas de la tele",
    )

