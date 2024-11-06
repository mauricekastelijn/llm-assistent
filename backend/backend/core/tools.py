import os

from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL
from langchain_community.tools import TavilySearchResults

from utils.logger import logger


class TavilySearchTool(TavilySearchResults):
    def __init__(self):
        if not os.getenv("TAVILY_API_KEY"):
            raise ValueError("TAVILY_API_KEY environment variable not set")

        super().__init__(
            max_results=5,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=True,
            include_images=False,
            # include_domains=[...],
            # exclude_domains=[...],
            # name="...",            # overwrite default tool name
            # description="...",     # overwrite default tool description
            # args_schema=...,       # overwrite default args_schema: BaseModel
        )

    async def ainvoke_tool_call_artifact(self, query):
        results = await self.ainvoke(
            {"args": {'query': query}, "type": "tool_call", "id": "foo", "name": "tavily"})
        return results.artifact


class PythonREPLTool(Tool):
    def __init__(self):
        super().__init__(
            name="python_repl",
            description="""
            A Python repl tool to execute python scripts.
            Use this to perform computations or solve problems through programming.
            Input should be a valid python command or script.
            Beware of syntax errors!
            Only use built-in python functions and libraries.
            If you want to see the output of a value,
            you should print it out with `print(...)`.
            """,
            func=PythonREPL().run,
        )


class ToolRegistry(object):
    def __init__(self):
        logger.info("Initializing tools...")
        self.tools = {}
        self.tools["tavily_search"] = TavilySearchTool()
        self.tools["python_repl"] = PythonREPLTool()

    def get_tools(self):
        return self.tools

    def get_search_tool(self):
        return self.tools["tavily_search"]

    def get_python_tool(self):
        return self.tools["python_repl"]
