import uvicorn
from fastapi import FastAPI

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

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
