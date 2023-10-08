from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
# internals
from app.services.news import drop_tables, create_tables
from app.routers import news, user, db, authentication

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "this is new"}


@app.post("/initdb")
async def initdb():
    try:
        drop_tables()
        create_tables()
        return {"message" : "Tables dropped and created!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error {e}"
        )


app.include_router(news.router)
app.include_router(user.router)
app.include_router(db.router)
app.include_router(authentication.router)