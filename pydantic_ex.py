from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()

# Here we are defining the schema for the post

class Post(BaseModel):
    title: str
    content: str
    # if user does not provide a value for it it will be default to True
    published: bool = True     # if default is provided the parameter becomes optional

    # You can Also Create an Optional parameter using the Optional library from the typing
    # library and provide the default data type of it and if we don't want to provide
    # any data if it is not sent then we can also default it to None
    rating: Optional[int] = None
@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}


# Here we are creating the post request where we are assigning the Body of the post
# request to the payload and then printing the payload
@app.post('/create_post')
def create_post(post: Post):
    # here this post variable is a pydantic model so if we want to create a dictionary
    # from it we can do it using the .dict() method on that pydantic model
    # :update: the .dict() method is deprecated now we use model_dump() instead
    # ex.
    post_dict = post.model_dump()
    print(post)
    return {"data": post_dict}

# title str, content str