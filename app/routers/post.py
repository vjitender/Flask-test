from fastapi import Depends, HTTPException, status, APIRouter, Response
from fastapi import FastAPI, status, HTTPException
from ..database import Base, engine, ToDo
from pydantic import BaseModel
from sqlalchemy.orm import Session


# Create ToDoRequest Base Model
class ToDoRequest(BaseModel):
    task: str

# Create the database
Base.metadata.create_all(engine)

# Initialize app
router = APIRouter()

@router.get("/")
def root():
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)
    # get the todo item with the given id
    todo = session.query(ToDo)
    return todo.all()


@router.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo: ToDoRequest):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the ToDo database model
    tododb = ToDo(task = todo.task)

    # add it to the session and commit it
    session.add(tododb)
    session.commit()

    # close the session
    session.close()

    task_dict = {
        "task": todo.task,
        "id": tododb.id
    }
    # return the id
    return task_dict

@router.get("/todo/{id}")
def read_todo(id: int):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the todo item with the given id
    todo = session.query(ToDo).get(id)

    # close the session
    session.close()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo

@router.put("/todo/{id}")
def update_todo(id: int, todo: ToDoRequest):
    session = Session(bind=engine, expire_on_commit=False)
    # get the todo item with the given id
    todo_obj = session.query(ToDo).get(id)
    todo_obj.task = todo.task
    session.commit()
    session.close()
    return f"update todo item with id {id}"

@router.delete("/todo/{id}")
def delete_todo(id: int):
    session = Session(bind=engine, expire_on_commit=False)
    todo_obj = session.query(ToDo).get(id)
    session.delete(todo_obj)
    session.commit()
    return f"delete todo item with id {id}"

@router.get("/todo")
def read_todo_list():
    return "read todo list"
