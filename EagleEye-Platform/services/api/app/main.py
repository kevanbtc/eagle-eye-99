from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from .routers import accounts, contacts, projects, files, estimates, assist

app = FastAPI(title="EagleEye API", version="1.0.0")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(accounts.router)
app.include_router(contacts.router)
app.include_router(projects.router)
app.include_router(files.router)
app.include_router(estimates.router)
app.include_router(assist.router)

@app.get("/")
def root():
    return {"ok": True, "service": "eagleeye-api"}
