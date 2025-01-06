import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from api import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.mount("/static", StaticFiles(directory="uploads"), name="static")

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
