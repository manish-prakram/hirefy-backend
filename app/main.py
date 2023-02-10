from fastapi import FastAPI, Request
from . import models
from .database import engine
from .routers import users, candidate, auth, recruiter, post, company

from .routers.user_route import soft_skills, technical_skills, education, experience, certificates, projects

from .config import settings
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from fastapi.templating import Jinja2Templates
# models.Base.metadata.create_all(bind=engine)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
app = FastAPI(title='Hire Block')

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates/")


origins = [
    "*",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    'https://dev7210.d27c7alg801bz2.amplifyapp.com',
    'http://127.0.0.1:8000',
    'http://127.0.0.1',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(candidate.router)
app.include_router(recruiter.router)
app.include_router(post.router)
app.include_router(company.router)
app.include_router(technical_skills.router)
app.include_router(soft_skills.router)
app.include_router(education.router)
app.include_router(experience.router)
app.include_router(certificates.router)
app.include_router(projects.router)


@app.get('/', response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})


handler = Mangum(app=app)
