
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent

from utils.logger import logger
from .models import ModelRegistry
from .tools import ToolRegistry


class EventsAgent(object):
    def __init__(self, model, search_tool):
        super().__init__()
        prompt = ChatPromptTemplate.from_template(
            "Generate a list of events and short descriptions happening in {location} on {date}")
        agent = create_react_agent(model, [search_tool])
        self.chain = prompt | agent

    async def ainvoke(self, location, date):
        logger.info(
            f"EventsAgent: Getting events for location: {location} and date: {date}")
        data = {"location": location, "date": date}
        result = await self.chain.ainvoke(data)
        logger.info(f"EventsAgent: Events response: {result}")
        return result["messages"][-1].content


class PythonAgent(object):
    def __init__(self, model, python_tool):
        super().__init__()
        prompt = ChatPromptTemplate.from_template(
            """
            Answer the user's query, using the python_repl tool if needed.
            Don't include python code in your answer.
            Instead, execute it using the python_repl tool using a tool call.
            Make sure to include the result in your final answer.
            The user query is: {query}
            """)
        agent = create_react_agent(model, [python_tool])
        self.chain = prompt | agent

    async def ainvoke(self, query):
        logger.info(f"PythonAgent: Answering query: {query}")
        result = await self.chain.ainvoke(query)
        logger.info(f"PythonAgent: Query response: {result}")
        return result["messages"][-1].content


class AgentRegistry(object):
    def __init__(self, models: ModelRegistry, tools: ToolRegistry):
        logger.info("Initializing agents...")
        self.agents = {}
        self.agents['events_agent'] = EventsAgent(
            models.get_chat_model(), tools.get_search_tool())
        self.agents['python_agent'] = PythonAgent(
            models.get_chat_model(), tools.get_python_tool())

    def get_agents(self):
        return self.agents
