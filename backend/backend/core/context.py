from .models import ModelRegistry
from .tools import ToolRegistry
from .chains import ChainRegistry
from .agents import AgentRegistry

from utils.logger import logger


class Context(object):
    # Define this class as a singleton
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Context, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.models = ModelRegistry()
        self.tools = ToolRegistry()
        self.chains = ChainRegistry(self.models, self.tools)
        self.agents = AgentRegistry(self.models, self.tools)
