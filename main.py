from fastapi import FastAPI
import uvicorn
from config.database import engine
from routers import blog, user
from models import models 

app = FastAPI()

models.Base.metadata.create_all(engine)


app.include_router(blog.router)
app.include_router(user.router)







if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info", reload=True)