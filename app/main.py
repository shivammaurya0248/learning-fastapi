from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["https://www.google.com",]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#
# my_posts = [
#     {
#         "id": 1,
#         "title": "title of post 1",
#         "content": "content of post 1"
#     },
#     {
#         "id": 2,
#         "title": "favorite food",
#         "content": "I like pizza"
#     },
# ]
#
#
# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
#
#
# def find_index_post(id):
#     for index, post in enumerate(my_posts):
#         if post['id'] == id:
#             return index


