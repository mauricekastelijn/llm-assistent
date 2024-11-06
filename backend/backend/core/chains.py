
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.logger import logger

from .models import ModelRegistry
from .tools import ToolRegistry

from pydantic import BaseModel
from typing_extensions import List


class JokeChain(object):
    def __init__(self, model):
        super().__init__()
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


class AdjacentQueriesChain(object):

    class SearchQueryList(BaseModel):
        """List of search queries adjacent to a common query."""
        queries: List[str]

    def __init__(self, model):
        prompt = ChatPromptTemplate.from_template(
            """
            List {num_results} new adjacent search queries related to the query
            '{query}', in the form of questions.

            Your existing knowledge on the query is given below. The new search
            queries must search for data not yet covered your existing
            knowledge.

            Output format: JSON list of strings according to schema:
            {{
                "queries": [
                    "query1",
                    "query2",
                    ...
                ]
            }}

            The existing knowledge is given below:
            {knowledge}
            """)
        self.parser = PydanticOutputParser(
            pydantic_object=AdjacentQueriesChain.SearchQueryList)
        self.chain = prompt | model | self.parser

    async def ainvoke(self, query, num_results, knowledge=None):
        logger.info(f"AdjacentQueriesChain: Getting queries for: {query}")
        result = await self.chain.ainvoke({"query": query,
                                           "num_results": num_results,
                                           "knowledge": knowledge})
        logger.info(f"AdjacentQueriesChain: Response: {result}")
        return result.queries

    def get_chain(self):
        return self.chain


class SummaryChain(object):

    def __init__(self, model):
        prompt = ChatPromptTemplate.from_template(
            """
            Write an essay on the subject '{subject}' based on the knowledge
            given below. Organize the content in a coherent manner and ensure
            that the essay is informative and engaging. DO NOT make up
            information. Use only the information provided in the knowledge
            section.

            Your existing knowledge on the subject is given below:
            {knowledge}
            """)
        self.chain = prompt | model | StrOutputParser()

    async def ainvoke(self, subject, knowledge):
        logger.info(f"SummaryChain: Creating summary for: {subject}")
        result = await self.chain.ainvoke({"subject": subject,
                                           "knowledge": knowledge})
        logger.info(f"SummaryChain: Response: {result}")
        return result

    def get_chain(self):
        return self.chain


class ChainRegistry(object):
    def __init__(self, models: ModelRegistry, tools: ToolRegistry):
        logger.info("Initializing chains...")
        self.chains = {}
        self.chains['joke_chain'] = JokeChain(models.get_chat_model())
        self.chains['adjacent_queries_chain'] = AdjacentQueriesChain(
            models.get_chat_model_json())
        self.chains['summary_chain'] = SummaryChain(models.get_chat_model())

    def get_chains(self):
        return self.chains
