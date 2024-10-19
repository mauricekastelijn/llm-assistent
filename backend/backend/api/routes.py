from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from core.context import Context
from services.business_logic import get_joke, get_events
from utils.logger import logger
from .schemas import JokeRequestSchema, EventsRequestSchema, ResponseSchema

api_router = APIRouter()


@api_router.post("/joke")
async def joke_request(
    request: JokeRequestSchema, context: Annotated[Context, Depends()]
) -> ResponseSchema:
    logger.info(f"Called endpoint /joke with request: {request}")
    response = await get_joke(context, request.text)
    return {"text": response}


@api_router.post("/events")
async def events_request(
    request: EventsRequestSchema, context: Annotated[Context, Depends()]
) -> ResponseSchema:
    logger.info(f"Called endpoint /events with request: {request}")
    response = await get_events(context, request.location, request.date)
    return {"text": response}


@api_router.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Joke Generator</title>
    </head>
    <body>
        <h1>Joke Generator</h1>
        <input type="text" id="jokeInputText" placeholder="Enter your text here">
        <button onclick="tellJoke()">Tell Joke</button>
        <h1>Find events</h1>
        <input type="text" id="locationInputText" placeholder="Enter your location here">
        <input type="text" id="dateInputText" placeholder="Enter your date here">
        <button onclick="getEvents()">Get events</button>
        <p id="responseText"></p>
        <script>
            async function tellJoke() {
                const jokeInputText = document.getElementById('jokeInputText').value;
                const response = await fetch('/joke', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ text: jokeInputText })
                });
                const data = await response.json();
                document.getElementById('responseText').innerText = data.text;
            }
        </script>
        <script>
            async function getEvents() {
                const locationInputText = document.getElementById('locationInputText').value;
                const dateInputText = document.getElementById('dateInputText').value;
                const response = await fetch('/events', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ location: locationInputText, date: dateInputText })
                });
                const data = await response.json();
                document.getElementById('responseText').innerText = data.text;
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
