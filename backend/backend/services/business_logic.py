from core.context import Context

from utils.logger import logger

import json


async def get_test_result(context: Context, subject: str):
    logger.info(f"Getting test result for subject: {subject}")

    adjacent_chain = context.chains.get_chains()['adjacent_queries_chain']
    search_tool = context.tools.get_search_tool()
    summary_chain = context.chains.get_chains()['summary_chain']

    knowledge = []
    for iter in range(1):
        queries = await adjacent_chain.ainvoke(subject, 4,
                                               knowledge="\n".join(knowledge))
        responses = []
        for query in queries:
            artifact = await search_tool.ainvoke_tool_call_artifact(query)
            response = {"query": query, "answer": artifact["answer"]}

            if False:
                summary = await summary_chain.ainvoke(query,
                                                      "\n".join(result["raw_content"]
                                                                for result in artifact["results"]
                                                                if result["raw_content"]))
                response["summary"] = summary

            responses.append(response)
            knowledge.extend([f"Query: {response["query"]}",
                              f"Answer: {response["answer"]}",
                              "========"])

        logger.info(f"Responses iter {iter}: {
                    json.dumps(responses, indent=4)}")

    # summarize knowledge into result
    result = await summary_chain.ainvoke(subject, "\n".join(knowledge))
    return result


async def get_joke(context: Context, subject: str):
    logger.info(f"Getting joke for subject: {subject}")
    chain = context.chains.get_chains()['joke_chain']
    response = await chain.ainvoke(subject)
    logger.info(f"Joke response: {response}")

    return response


async def get_events(context: Context, location: str, date: str):
    logger.info(f"Getting events for location: {location} and date: {date}")
    agent = context.agents.get_agents()['events_agent']
    response = await agent.ainvoke(location, date)
    logger.info(f"Events response: {response}")

    return response


async def get_query_result(context: Context, query: str):
    logger.info(f"Answering the query: {query}")
    agent = context.agents.get_agents()['python_agent']
    response = await agent.ainvoke(query)
    logger.info(f"Query response: {response}")

    return response


async def add_github_comment(context: Context, repo: str, pr_number: int,
                             request: str):
    logger.info(f"Adding comment to PR #{pr_number} in repo {
                repo}; request: {request}")
    agent = context.agents.get_agents()['github_comment_agent']
    response = await agent.ainvoke(repo, pr_number, request)
    logger.info(f"GitHub comment response: {response}")
    return response


async def review_github_pr(context: Context, repo: str, pr_number: int):
    logger.info(f"Reviewing PR #{pr_number} in repo {repo}")
    agent = context.agents.get_agents()['github_pullrequest_patch_review_agent']
    response = await agent.ainvoke(repo, pr_number)
    logger.info("GitHub PR review completed")
    return response
