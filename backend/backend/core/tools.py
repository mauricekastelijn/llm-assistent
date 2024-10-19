
from langchain_community.tools import TavilySearchResults

from utils.logger import logger
import os


class TavilySearchTool(TavilySearchResults):
    def __init__(self):
        if not os.getenv("TAVILY_API_KEY"):
            raise ValueError("TAVILY_API_KEY environment variable not set")

        super().__init__(
            max_results=5,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=False,
            include_images=False,
            # include_domains=[...],
            # exclude_domains=[...],
            # name="...",            # overwrite default tool name
            # description="...",     # overwrite default tool description
            # args_schema=...,       # overwrite default args_schema: BaseModel
        )


class ToolRegistry(object):
    def __init__(self):
        logger.info("Initializing tools...")
        self.tools = {}
        self.tools['tavily_search'] = TavilySearchTool()

    def get_tools(self):
        return self.tools

    def get_search_tool(self):
        return self.tools['tavily_search']
