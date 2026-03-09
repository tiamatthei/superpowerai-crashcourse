from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(default="hola mundo", description="El contenido del mensaje")

