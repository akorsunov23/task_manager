import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Task manger")


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", log_level="info")
