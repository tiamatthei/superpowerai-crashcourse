from pydantic_ai import format_as_xml, Agent
from weather.system_prompt import prompt
from .tools import weather_tools


agent = Agent(
    "google-gla:gemini-2.5-flash",
    toolsets=[weather_tools],
)

agent.instrument_all()


@agent.system_prompt
async def system_prompt():
    return format_as_xml(prompt)
