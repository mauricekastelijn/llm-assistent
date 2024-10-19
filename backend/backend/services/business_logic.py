from core.context import Context

from utils.logger import logger


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
