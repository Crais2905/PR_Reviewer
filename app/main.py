from fastapi import FastAPI

from app.db.session import engine
from app.db.models import Base

from app.routes.user import router as user_router
from app.routes.review import router as review_router

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(user_router, prefix="/auth", tags=["Auth"])
app.include_router(review_router, prefix="/reviews", tags=["Review"])
