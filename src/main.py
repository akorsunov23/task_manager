import uvicorn
from fastapi import FastAPI

from src.assign_tasks.routers import assign_task_app
from src.auth.routers import auth_app
from src.tasks.routers import task_app

app = FastAPI(title="Task manager")

app.include_router(auth_app)
app.include_router(task_app)
app.include_router(assign_task_app)


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        reload=True,
        host="127.0.0.1",
        log_level="info"
    )
