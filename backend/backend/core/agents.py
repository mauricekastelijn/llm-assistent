
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


class AgentRegistry(object):
    def __init__(self, models: ModelRegistry, tools: ToolRegistry):
        logger.info("Initializing agents...")
        self.agents = {}
        self.agents['events_agent'] = EventsAgent(
            models.get_chat_model(), tools.get_search_tool())

    def get_agents(self):
        return self.agents
