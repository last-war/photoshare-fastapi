from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.database.db import get_db
from src.routes import users, comments, tags, images, ratings

app = FastAPI()


@app.get("/", response_class=HTMLResponse, description='Main page')
def root():
    return {"message": "Welcome to the FAST API from team 6"}


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    """
    Health Checker

    :param db: database session
    :return: health status
    :rtype: dict
    """
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


app.include_router(users.router, prefix='/api')
app.include_router(comments.router, prefix='/api')
app.include_router(images.router, prefix='/api')
app.include_router(tags.router, prefix='/api')
app.include_router(ratings.router, prefix='/api')


