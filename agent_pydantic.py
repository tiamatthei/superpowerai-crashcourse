from pydantic import BaseModel, Field
from pydantic_ai import format_as_xml, Agent

def fetch_from_jira():
    pass

def fetch_from_github():
    pass

def run_test(test_name: str):
    pass

agent = Agent(
    name="JiraAgent",
    description="An agent that decides which tests to run based on the latest issues from Jira, and the latest commits from GitHub",
    tools=[fetch_from_jira, fetch_from_github, run_test],
    model="gemini-2.5-flash",
)

response = agent.run("Fetch the latest issues from Jira and the latest commits from GitHub")
print(response)

