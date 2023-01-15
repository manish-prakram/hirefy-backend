from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, auth, recruiter, post

from .config import settings
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(recruiter.router)
app.include_router(post.router)


@app.get('/')
def root():
    return {"message": "Hello  😁 "}

handler = Mangum(app=app)