from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True     # if default is provided the parameter becomes optional
    # rating: Optional[int] = None

my_posts = [
    {
        "id": 1,
        "title": "title of post 1",
        "content": "content of post 1"
    },
    {
        "id": 2,
        "title": "favorite food",
        "content": "I like pizza"
    },
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():

    return {"data": my_posts}


# You can also change the default status code in the decorator
# like below
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post, response: Response):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    return my_posts[-1]


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)

    if not post:
        # response.status_code = 404
        # we can directly give http status code, or
        # we can use status library from the fastapi
        # so that we don't have to remember all the codes

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with the id {id} not found"}

        # we can also do all this with HTTPException module
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')

    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    # deleting post
    post_index = find_index_post(id)
    if post_index:
        my_posts.pop(post_index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Post with id : {id} does not exist")


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Post with id : {id} does not exist")

    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    print(post)
    return {"data": post_dict}