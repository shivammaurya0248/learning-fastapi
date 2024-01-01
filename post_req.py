from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}


# Here we are creating the post request where we are assigning the Body of the post
# request to the payload and then printing the payload
@app.post('/create_post')
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"newpost": f"title: {payload['title']} content: {payload['content']}"}
