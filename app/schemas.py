from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel


class TodosSchema(BaseModel):
    """
    Todos schema.
    """
    id: UUID
    title: str
    description: str | None = None
    done: datetime


class CreateRequestSchema(BaseModel):
    title: str
    description: str | None = None
    done: datetime


class UpdateRequestSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    done: datetime | None = None


def doc_to_schema(doc: dict) -> TodosSchema:
    return TodosSchema(
        id=UUID(doc["_id"]),
        title=doc["title"],
        description=doc.get("description"),
        done=doc["done"],
    )


def create_to_doc(data: CreateRequestSchema) -> dict:
    todo_id = uuid4()
    return {
        "_id": str(todo_id),
        "title": data.title,
        "description": data.description,
        "done": data.done,
    }