from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent

from utils.logger import logger
from .models import ModelRegistry
from .tools import ToolRegistry
from .chains import ChainRegistry


class EventsAgent(object):
    def __init__(self, model, search_tool):
        super().__init__()
        prompt = ChatPromptTemplate.from_template(
            "Generate a list of events and short descriptions happening in {location} on {date}"
        )
        agent = create_react_agent(model, [search_tool])
        self.chain = prompt | agent

    async def ainvoke(self, location, date):
        logger.info(
            f"EventsAgent: Getting events for location: {
                location} and date: {date}"
        )
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
            """
        )
        agent = create_react_agent(model, [python_tool])
        self.chain = prompt | agent

    async def ainvoke(self, query):
        logger.info(f"PythonAgent: Answering query: {query}")
        result = await self.chain.ainvoke(query)
        logger.info(f"PythonAgent: Query response: {result}")
        return result["messages"][-1].content


class GitHubCommentAgent(object):
    def __init__(self, model, github_tool):
        super().__init__()
        prompt = ChatPromptTemplate.from_template(
            """
Add a comment to the GitHub pull request.
The repository is: {repo}
The pull request number is: {pr_number}
The request is: {request}

Use the github_comment tool to add the comment.
Formulate the comment text based on the request.
            """
        )
        agent = create_react_agent(model, [github_tool])
        self.chain = prompt | agent

    async def ainvoke(self, repo, pr_number, request):
        logger.info(
            f"GitHubCommentAgent: Adding comment to PR #{
                pr_number} in repo {repo}"
        )
        data = {"repo": repo, "pr_number": pr_number, "request": request}
        result = await self.chain.ainvoke(data)
        logger.info(f"GitHubCommentAgent: Comment added to PR #{pr_number}")
        return result["messages"][-1].content


class GitHubPullRequestReviewAgent(object):
    def __init__(self, model, get_files_tool, patch_review_chain, patch_comment_tool):
        super().__init__()
        self.get_files_tool = get_files_tool
        self.patch_review_chain = patch_review_chain
        self.patch_comment_tool = patch_comment_tool
        self.model = model

    async def ainvoke(self, repo, pr_number):
        logger.info(
            f"GitHubPullRequestReviewAgent: Reviewing code for PR #{
                pr_number} in repo {repo}"
        )

        # Fetch the pull request files
        pr_files = self.get_files_tool.get_pr_files(repo, pr_number)

        results = []
        for file in pr_files:
            contents = file["contents"]
            path = file["filename"]
            for start, end, header, content in file["hunks"]:
                patch = header + content
                comments = await self.patch_review_chain.ainvoke(
                    contents, start, end, patch
                )

                for comment in comments.comments if comments else []:
                    result = self.patch_comment_tool.add_patch_comment(
                        repo, pr_number, comment.content, path, comment.line)
                    results.append(result)

        logger.info(
            f"GitHubPullRequestReviewAgent: Code review completed for PR #{
                pr_number}"
        )
        return results


class AgentRegistry(object):
    def __init__(
        self, models: ModelRegistry, tools: ToolRegistry, chains: ChainRegistry
    ):
        logger.info("Initializing agents...")
        self.agents = {}
        self.agents["events_agent"] = EventsAgent(
            models.get_chat_model(), tools.get_search_tool()
        )
        self.agents["python_agent"] = PythonAgent(
            models.get_chat_model(), tools.get_python_tool()
        )
        self.agents["github_comment_agent"] = GitHubCommentAgent(
            models.get_chat_model(), tools.get_github_comment_tool()
        )
        self.agents["github_pullrequest_patch_review_agent"] = (
            GitHubPullRequestReviewAgent(
                models.get_chat_model(),
                tools.get_github_pr_files_tool(),
                chains.get_chains()["patch_review_chain"],
                tools.get_github_pr_patch_comment_tool(),
            )
        )

    def get_agents(self):
        return self.agents
