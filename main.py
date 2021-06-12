from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.get('/')
def index():
    return "Hello From FastAPI!"


@app.get('/about')
def about():
    return { 
        "data": { "Greet": "Welcome To About Page!" }
    }


@app.get('/blog/{id}')
def blog(id:int):
    return f"Get single blog of ID: {id}"


@app.post('/blog')
def create_blog(request: Blog):
    return request







if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info", reload=True)