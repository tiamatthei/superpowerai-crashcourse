from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logfire

import os
from dotenv import load_dotenv

load_dotenv()
if not os.environ.get("GOOGLE_API_KEY") and os.environ.get("GEMINI_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]


from pydantic_ai.ag_ui import AGUIApp
from app.agents import weather_agent


logfire.configure()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/weather-agent", AGUIApp(weather_agent))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
