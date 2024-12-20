import os
import re

from pydantic import BaseModel, Field
from typing import Optional, Type

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain_core.tools import Tool, BaseTool
from langchain_experimental.utilities import PythonREPL
from langchain_community.tools import TavilySearchResults
from github import Github, GithubException

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
            {
                "args": {"query": query},
                "type": "tool_call",
                "id": "foo",
                "name": "tavily",
            }
        )
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


class GitHubCommentTool(BaseTool):
    """
    A tool to add comments to GitHub pull requests.
    """

    class Comment(BaseModel):
        repo: str = Field(..., description="The repository name in 'owner/repo' format")
        pr_number: int = Field(..., description="The pull request number")
        comment: str = Field(..., description="The comment to add")

    name: str = "github_pullrequest_comment"
    description: str = "A tool to add comments to GitHub pull requests."
    args_schema: Type[BaseModel] = Comment

    def __init__(self, token, **kwargs):
        super().__init__(**kwargs)
        self._github = Github(token)

    def _run(
        self,
        repo: str,
        pr_number: int,
        comment: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        """Add a comment to a GitHub pull request."""
        logger.info(
            f"GitHubCommentTool: Adding comment to PR #{pr_number} in repo {
                repo}; comment: {comment}"
        )
        repository = self._github.get_repo(repo)
        pull_request = repository.get_pull(pr_number)
        result = pull_request.create_issue_comment(comment)
        return {"status": "success", "result": str(result)}


class GitHubPullRequestFilesTool(BaseTool):
    """
    A tool to get files from GitHub pull requests.
    """

    class FilesRequest(BaseModel):
        repo: str = Field(..., description="The repository name in 'owner/repo' format")
        pr_number: int = Field(..., description="The pull request number")

    name: str = "github_pullrequest_files"
    description: str = "A tool to get files from GitHub pull requests."
    args_schema: Type[BaseModel] = FilesRequest

    def __init__(self, token, **kwargs):
        super().__init__(**kwargs)
        self._github = Github(token)

    def _run(self, repo: str, pr_number: int):
        return self.get_pr_files(repo, pr_number)

    def get_pr_files(self, repo, pr_number):
        repo = self._github.get_repo(repo)
        pr = repo.get_pull(pr_number)
        commit = pr.get_commits().reversed[0]
        files = []
        for file in pr.get_files():
            contents = self.get_file_contents(repo, commit, file.filename)
            print(file.patch)
            hunks = self.extract_hunks(file.patch)
            print(hunks)
            files.append(
                {
                    "filename": file.filename,
                    "additions": file.additions,
                    "deletions": file.deletions,
                    "changes": file.changes,
                    "status": file.status,
                    "hunks": hunks,
                    "contents": contents,
                }
            )
        return files

    def get_file_contents(self, repo, commit, file_path):
        file_content = repo.get_contents(file_path, ref=commit.sha)
        return file_content.decoded_content.decode("utf-8")

    def extract_hunks(self, patch):
        """
        Return a list of hunks from a patch.
        A hunk is a tuple of (start, end, content), where 'content' includes
        the full hunk with the header and markers.
        """
        # Regular expression to match hunk headers and their content
        hunk_pattern = re.compile(
            r"(^@@ -\d+(?:,\d+)? \+\d+(?:,\d+)? @@(?:.+?)\n)"  # Hunk header
            r"(.+?)"  # Hunk content
            r"(?=\n@@|\Z)",  # Lookahead for next hunk or end of patch
            re.DOTALL | re.MULTILINE,
        )

        # Find all hunks in the patch
        matches = hunk_pattern.findall(patch)
        print(patch)
        print(matches)

        extracted_hunks = []
        for header, content in matches:
            # Extract the starting line number from the header
            match = re.search(r"\+(\d+)", header)
            if match:
                start = int(match.group(1))
                # Calculate the end line number based on the content
                end = start + sum(
                    1 for line in content.splitlines() if line.startswith(("+", " "))
                )
                # Combine header and content for the full hunk
                extracted_hunks.append((start, end, header, content))

        return extracted_hunks


class GitHubPullRequestPatchCommentTool(BaseTool):
    """
    A tool to add code comments to GitHub pull requests patches.
    """

    class Comment(BaseModel):
        repo: str = Field(..., description="The repository name in 'owner/repo' format")
        pr_number: int = Field(..., description="The pull request number")
        comment: str = Field(..., description="The comment text to add")
        path: str = Field(..., description="The file path to comment on")
        line: int = Field(..., description="The line number to comment on")

    name: str = "github_pullrequest_patch_comment"
    description: str = "A tool to add code comments to GitHub pull requests patches."
    args_schema: Type[BaseModel] = Comment

    def __init__(self, token, **kwargs):
        super().__init__(**kwargs)
        self._github = Github(token)

    def _run(self, repo, pr_number, comment, path, line):
        return self.add_patch_comment(repo, pr_number, comment, path, line)

    def add_patch_comment(self, repo, pr_number, comment, path, line):
        repo = self._github.get_repo(repo)
        pr = repo.get_pull(pr_number)
        commit = pr.get_commits().reversed[0]
        try:
            result = pr.create_review_comment(
                body=comment, commit=commit, path=path, line=line
            )
            return {"status": "success", "result": str(result)}
        except GithubException as e:
            return {"status": "error", "message": str(e)}


class ToolRegistry(object):
    def __init__(self):
        logger.info("Initializing tools...")

        github_token = os.getenv("GITHUB_TOKEN", None)

        self.tools = {}
        self.tools["tavily_search"] = TavilySearchTool()
        self.tools["python_repl"] = PythonREPLTool()
        self.tools["github_comment"] = (
            GitHubCommentTool(github_token) if github_token else None
        )
        self.tools["github_pr_files"] = (
            GitHubPullRequestFilesTool(github_token) if github_token else None
        )
        self.tools["github_pr_patch_comment"] = (
            GitHubPullRequestPatchCommentTool(github_token) if github_token else None
        )

    def get_tools(self):
        return self.tools

    def get_search_tool(self):
        return self.tools["tavily_search"]

    def get_python_tool(self):
        return self.tools["python_repl"]

    def get_github_comment_tool(self):
        return self.tools["github_comment"]

    def get_github_pr_files_tool(self):
        return self.tools["github_pr_files"]

    def get_github_pr_patch_comment_tool(self):
        return self.tools["github_pr_patch_comment"]
