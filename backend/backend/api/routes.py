from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from core.context import Context
from services.business_logic import \
    get_test_result, get_joke, get_events, get_query_result
from utils.logger import logger
from .schemas import QueryRequestSchema, EventsRequestSchema, ResponseSchema

api_router = APIRouter()


@api_router.post("/test")
async def test_request(
    request: QueryRequestSchema, context: Annotated[Context, Depends()]
) -> ResponseSchema:
    logger.info(f"Called endpoint /test with request: {request}")
    response = await get_test_result(context, request.text)
    return {"text": response}


@api_router.post("/joke")
async def joke_request(
    request: QueryRequestSchema, context: Annotated[Context, Depends()]
) -> ResponseSchema:
    logger.info(f"Called endpoint /joke with request: {request}")
    response = await get_joke(context, request.text)
    return {"text": response}


@api_router.post("/query")
async def query_request(
    request: QueryRequestSchema, context: Annotated[Context, Depends()]
) -> ResponseSchema:
    logger.info(f"Called endpoint /query with request: {request}")
    response = await get_query_result(context, request.text)
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
    <title>LLM Application</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #121212;
            color: #e0e0e0;
        }
        h1 {
            color: #ffffff;
            font-size: 24px;
        }
        input[type="text"] {
            width: 100%;
            max-width: 500px;
            padding: 12px;
            margin: 12px 0;
            box-sizing: border-box;
            font-size: 16px;
            background-color: #333;
            color: #e0e0e0;
            border: 1px solid #555;
            border-radius: 5px;
        }
        button {
            padding: 12px 24px;
            margin: 12px 0;
            font-size: 16px;
            background-color: #1f8e3f;
            color: #ffffff;
            border: none;
            cursor: pointer;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #176a2d;
        }
        .response-container {
            margin-top: 20px;
            position: relative;
            max-width: 600px;
        }
        #responseText {
            padding: 15px;
            font-size: 16px;
            background-color: #333;
            color: #e0e0e0;
            border: 1px solid #555;
            border-radius: 5px;
            max-height: 300px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
            resize: vertical;
        }
        .toggle-wrap-btn, .copy-btn {
            padding: 5px 10px;
            font-size: 14px;
            color: #e0e0e0;
            background-color: #555;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-right: 5px;
        }
        .toggle-wrap-btn:hover, .copy-btn:hover {
            background-color: #777;
        }
        .controls {
            display: flex;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h1>Test Result</h1>
    <input type="text" id="testInputText" placeholder="Enter your text here">
    <button onclick="getTestOutput()">Test</button>

    <h1>Joke Generator</h1>
    <input type="text" id="jokeInputText" placeholder="Enter your text here">
    <button onclick="tellJoke()">Tell Joke</button>

    <h1>Query Python Agent</h1>
    <input type="text" id="queryText" placeholder="Enter your query here">
    <button onclick="query()">Query</button>

    <h1>Find Events</h1>
    <input type="text" id="locationInputText" placeholder="Enter your location here">
    <input type="text" id="dateInputText" placeholder="Enter your date here">
    <button onclick="getEvents()">Get Events</button>

    <div class="response-container">
        <div id="responseText">Your response will appear here...</div>
        <div class="controls">
            <button class="toggle-wrap-btn" onclick="toggleWordWrap()">Toggle Word Wrap</button>
            <button class="copy-btn" onclick="copyToClipboard()">Copy to Clipboard</button>
        </div>
    </div>

    <script>
        function toggleWordWrap() {
            const responseText = document.getElementById('responseText');
            if (responseText.style.whiteSpace === 'pre-wrap') {
                responseText.style.whiteSpace = 'pre';
                responseText.style.wordWrap = 'normal';
            } else {
                responseText.style.whiteSpace = 'pre-wrap';
                responseText.style.wordWrap = 'break-word';
            }
        }

        function copyToClipboard() {
            const responseText = document.getElementById('responseText').innerText;
            navigator.clipboard.writeText(responseText)
                .then(() => alert("Copied to clipboard!"))
                .catch(() => alert("Failed to copy."));
        }
    </script>

    <script>
        async function getTestOutput() {
            const testInputText = document.getElementById('testInputText').value;
            const response = await fetch('/test', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: testInputText })
            });
            const data = await response.json();
            document.getElementById('responseText').innerText = data.text;
        }

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

        async function query() {
            const queryText = document.getElementById('queryText').value;
            const response = await fetch('/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: queryText })
            });
            const data = await response.json();
            document.getElementById('responseText').innerText = data.text;
        }

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
