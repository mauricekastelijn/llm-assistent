
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from utils.logger import logger

from .models import ModelRegistry
from .tools import ToolRegistry


class JokeChain(object):
    def __init__(self, model):
        super().__init__()
        model = model
        prompt = ChatPromptTemplate.from_template(
            "tell me a joke about {subject}")
        self.chain = prompt | model | StrOutputParser()

    async def ainvoke(self, subject):
        logger.info(f"JokeChain: Getting joke for subject: {subject}")
        result = await self.chain.ainvoke(subject)
        logger.info(f"JokeChain: Joke response: {result}")
        return result

    def get_chain(self):
        return self.chain


class ChainRegistry(object):
    def __init__(self, models: ModelRegistry, tools: ToolRegistry):
        logger.info("Initializing chains...")
        self.chains = {}
        self.chains['joke_chain'] = JokeChain(models.get_chat_model())

    def get_chains(self):
        return self.chains
