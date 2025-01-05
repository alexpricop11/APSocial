import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from password_service.routes import password
from posts.comments.routes import comment
from posts.images.routes import post
from users.auth.routes import auth
from users.profile.routes import user

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth)
app.include_router(user)
app.include_router(post)
app.include_router(password)
app.include_router(comment)
app.mount("/static", StaticFiles(directory="uploads"), name="static")

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
