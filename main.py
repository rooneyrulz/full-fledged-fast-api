from fastapi import FastAPI
import uvicorn

app = FastAPI()


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







if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info", reload=True)