from fastapi import FastAPI


from app.routes.user_route import router as user_router

# from app.db.session import get_db
# from app.models.user import User

app = FastAPI()

app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
