from fastapi import FastAPI
from app.api.v1.api_v1 import api_router
from app.core.config import settings

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
    )

    # include API blueprints
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = create_app()

# For direct run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
