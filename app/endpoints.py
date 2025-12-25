from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from app.schemas import (
    TodosSchema,
    CreateRequestSchema,
    UpdateRequestSchema,
    create_to_doc,
    doc_to_schema,
)

router = APIRouter()


def get_db(request: Request):
    return request.app.state.mongo_db


@router.post("/", response_model=TodosSchema, status_code=status.HTTP_201_CREATED)
async def create_todo(data: CreateRequestSchema, db=Depends(get_db)):
    todos = db["todos"]
    doc = create_to_doc(data)
    await todos.insert_one(doc)
    return doc_to_schema(doc)


@router.put("/{todo_id}", response_model=TodosSchema)
async def update_todo(todo_id: UUID, data: UpdateRequestSchema, db=Depends(get_db)):
    todos = db["todos"]

    updates = {}
    if data.title is not None:
        updates["title"] = data.title
    if data.description is not None:
        updates["description"] = data.description
    if data.done is not None:
        updates["done"] = data.done

    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = await todos.find_one_and_update(
        {"_id": str(todo_id)},
        {"$set": updates},
        return_document=True,
    )

    if result is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    return doc_to_schema(result)


@router.get("/", response_model=list[TodosSchema])
async def get_all_todos(db=Depends(get_db)):
    todos = db["todos"]
    items = []
    async for doc in todos.find({}):
        items.append(doc_to_schema(doc))
    return items


@router.get("/{todo_id}", response_model=TodosSchema)
async def get_todo_by_id(todo_id: UUID, db=Depends(get_db)):
    todos = db["todos"]
    doc = await todos.find_one({"_id": str(todo_id)})
    if doc is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return doc_to_schema(doc)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: UUID, db=Depends(get_db)):
    todos = db["todos"]
    res = await todos.delete_one({"_id": str(todo_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
