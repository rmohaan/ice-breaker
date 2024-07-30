import os
from dotenv import load_dotenv
from tools.tools import get_profile_url_tavily

from langchain import hub
from langchain_community.chat_models import ChatOllama
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import ( create_react_agent, AgentExecutor )

load_dotenv()

def lookup(name: str, mock: bool = False) -> str:
    if mock:
        return "https://www.linkedin.com/in/eden-marco/"

    llm = ChatOllama(model="llama3")

    template = """given the full name {name_of_person} of the LinkedIn user, get me the LinkedIn profile url.
                Your answer should only contain a URL"""

    prompt_template = PromptTemplate (
        template=template,
        input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name = "Crawl Google for a LinkedIn profile page",
            func = get_profile_url_tavily,
            description = "useful for when you need to get the LinkedIn page URL"
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm = llm, tools=tools_for_agent, prompt=react_prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True)

    try:
        result = agent_executor.invoke( 
            input={"input": prompt_template.format_prompt(name_of_person=name)}
        )
    except Exception as e:
        result = str(e)
        if not result.startswith("Could not parse LLM output: `"):
            raise e
        result = result.removeprefix("Could not parse LLM output: `").removesuffix("`")

    linkedin_url = result["output"]
    return linkedin_url





