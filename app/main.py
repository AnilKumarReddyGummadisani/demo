from fastapi import FastAPI
from app.routes import items

app = FastAPI(
    title="Python CRUD Demo",
    description="A simple CRUD REST API built with FastAPI",
    version="1.0.0",
)

app.include_router(items.router, prefix="/api/v1/items", tags=["items"])


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "UP"}
