import uvicorn
from fastapi import FastAPI
from src.auth.routers import auth_app

app = FastAPI(title="Task manger")

app.include_router(auth_app)


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", log_level="info")
