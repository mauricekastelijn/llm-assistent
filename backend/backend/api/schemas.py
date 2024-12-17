from pydantic import BaseModel


class QueryRequestSchema(BaseModel):
    text: str


class EventsRequestSchema(BaseModel):
    location: str
    date: str


class ResponseSchema(BaseModel):
    text: str


class GitHubCommentRequestSchema(BaseModel):
    repo: str
    pr_number: int
    comment: str
