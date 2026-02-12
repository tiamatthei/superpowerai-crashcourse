from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from system_prompt import prompt
from pydantic_ai import format_as_xml

from dotenv import load_dotenv


load_dotenv()


@tool
def get_temperature(city: str = "Concepción", scale: str = "Celsius") -> float:
    """
    Gets the temperature for a given city and scale.
    """
    # llamaría a una API de clima para obtener la temperatura
    return 20.0


@tool
def get_humidity(city: str = "Concepción") -> int:
    """
    Gets the humidity for a given city.
    """
    # llamaría a una API de clima para obtener la humedad
    return 50


@tool
def get_wind_speed(city: str = "Concepción") -> float:
    """
    Gets the wind speed for a given city.
    """
    # llamaría a una API de clima para obtener la velocidad del viento
    return 10.0


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
agent = create_agent(llm, tools=[get_temperature, get_humidity, get_wind_speed], system_prompt = format_as_xml(prompt))

result = agent.invoke(
    {"messages": [HumanMessage(content="Como va a estar el clima hoy en conce?")]}
)
print(result["messages"][-1].content)
