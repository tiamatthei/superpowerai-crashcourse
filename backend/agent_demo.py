from pydantic_ai import Agent
from pydantic import BaseModel

agent = Agent(
    model="gemini-2.5-flash"
)

class Producto(BaseModel):
    id: int
    nombre: str
    precio: float
    stock: int
    descuento: float
    categoria: str



Producto(id=1, nombre="Producto 1", precio=10.0, stock=100, descuento=0.1, categoria="Electrónica")


@agent.tool_plain
async def trae_productos(nombre: str) -> Producto:
    return Producto(nombre="Producto 1", precio=10.0, stock=100, descuento=0.1, categoria="Electrónica")


# @agent.tool_plain
# async def elimina_producto(id: int) -> str:
#     return f"Producto eliminado: {id}"




