from pydantic import BaseModel


class JokeRequestSchema(BaseModel):
    text: str


class QueryRequestSchema(BaseModel):
    text: str


class EventsRequestSchema(BaseModel):
    location: str
    date: str


class ResponseSchema(BaseModel):
    text: str
