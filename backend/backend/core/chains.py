from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.logger import logger

from .models import ModelRegistry
from .tools import ToolRegistry

from pydantic import BaseModel, Field
from typing_extensions import List, Optional


class JokeChain(object):
    def __init__(self, models):
        super().__init__()
        prompt = ChatPromptTemplate.from_template("tell me a joke about {subject}")
        model = models.get_chat_model()
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

    def __init__(self, models):
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
            """
        )
        model = models.get_chat_model_json(
            format=self.SearchQueryList.model_json_schema()
        )
        parser = PydanticOutputParser(pydantic_object=self.SearchQueryList)
        self.chain = prompt | model | parser

    async def ainvoke(self, query, num_results, knowledge=None):
        logger.info(f"AdjacentQueriesChain: Getting queries for: {query}")
        result = await self.chain.ainvoke(
            {"query": query, "num_results": num_results, "knowledge": knowledge}
        )
        logger.info(f"AdjacentQueriesChain: Response: {result}")
        return result.queries

    def get_chain(self):
        return self.chain


class SummaryChain(object):

    def __init__(self, models):
        prompt = ChatPromptTemplate.from_template(
            """
Write an essay on the subject '{subject}' based on the knowledge
given below. Organize the content in a coherent manner and ensure
that the essay is informative and engaging. DO NOT make up
information. Use only the information provided in the knowledge
section.

Your existing knowledge on the subject is given below:
{knowledge}
            """
        )
        model = models.get_chat_model()
        self.chain = prompt | model | StrOutputParser()

    async def ainvoke(self, subject, knowledge):
        logger.info(f"SummaryChain: Creating summary for: {subject}")
        result = await self.chain.ainvoke({"subject": subject, "knowledge": knowledge})
        logger.info(f"SummaryChain: Response: {result}")
        return result

    def get_chain(self):
        return self.chain


class GitHubPullRequestPatchReviewChain(object):

    class ReviewComment(BaseModel):
        """Review comment."""

        content: Optional[str] = Field(
            default=None, description="The content of the review comment"
        )
        line: Optional[int] = Field(
            default=None, description="The line number to comment on"
        )

    def __init__(self, models):
        super().__init__()
        self.parser = PydanticOutputParser(pydantic_object=self.ReviewComment)
        prompt = ChatPromptTemplate.from_template(
            """
Output a helpful code review comment on the following code patch:
```
{patch}
```

Only make comments for lines that have been changed. Do not comment on
unmodified lines. Ensure that the comment is constructive and
provides actionable feedback.
Only provide major comments on the code. Do not provide minor
stylistic comments.
If you have no major comments, do not output anything.

For reference, the new code is given below:
```
{contents}
```

{format_instructions}
            """
        )
        model = models.get_chat_model_json()
        model = model.with_structured_output(self.ReviewComment)
        self.chain = prompt | model

    def chunk_with_line_numbers(self, contents, start, end):
        return "\n".join(
            [
                f"{start+i+1}: {line}"
                for i, line in enumerate(contents.split("\n")[start:end])
            ]
        )

    async def ainvoke(self, file_contents, start, end, patch_content) -> ReviewComment:
        logger.info(
            f"GitHubPullRequestPatchReviewChain: Reviewing code patch {
            patch_content} from line {start} to {end}"
        )
        chunk = self.chunk_with_line_numbers(
            file_contents, max(start - 10, 0), end + 10
        )
        result = await self.chain.ainvoke(
            {
                "patch": patch_content,
                "contents": chunk,
                "format_instructions": self.parser.get_format_instructions(),
            }
        )
        logger.info(f"GitHubPullRequestPatchReviewChain: Response: {result}")
        return result

    def get_chain(self):
        return self.chain


class ChainRegistry(object):
    def __init__(self, models: ModelRegistry, tools: ToolRegistry):
        logger.info("Initializing chains...")
        self.chains = {}
        self.chains["joke_chain"] = JokeChain(models)
        self.chains["adjacent_queries_chain"] = AdjacentQueriesChain(models)
        self.chains["summary_chain"] = SummaryChain(models)
        self.chains["patch_review_chain"] = GitHubPullRequestPatchReviewChain(models)

    def get_chains(self):
        return self.chains
