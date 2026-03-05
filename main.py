from fastapi import FastAPI
from pydantic_ai.ag_ui import AGUIApp
from app.agents import weather_agent


import os
from dotenv import load_dotenv

load_dotenv()
if not os.environ.get("GOOGLE_API_KEY") and os.environ.get("GEMINI_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]


app = FastAPI()


app.mount("/weather-agent", AGUIApp(weather_agent))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
