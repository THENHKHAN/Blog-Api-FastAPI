

#  This file contains some basic and starter code. It does do anything with the blog directory.

from fastapi import FastAPI,status
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

app = FastAPI()


class Blog(BaseModel):
    title: str
    post: str
    # published: Optional[bool] = False  or without bool = False will work the same
    published_at: str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


@app.get("/")
def index ():
       return {"message": "Hello World!"}

# query paramter
@app.get("/blog/unpublish/", status_code = 200)
def show_unpublish_post(limit : Optional[int] = 10, publish: Optional[bool] = False):
     return {"data": [{"details":f"{limit} unpublish post"} , {"limit" : limit}] }
     

# dynamic path parameter
@app.get("/blog/{id}", status_code=200)
async def showOnePost(id: int):
    return {"data": f" {id} blog post "}


# only 1o comment of a particular id block
@app.get("/blog/{id}/comments")
def comments (id:int, limit=10):
         # fetch comments of blog with id = id
    return {'data': {'1', '2',"4"}}
# {'1', '2'} convetred by fastapi into list evene without using []
'''
{
  "data": [
    "1",
    "2"
  ]
}
'''
     

# post request based on the pydantic Blog model  that we have created above  
@app.post("/blog/", status_code=201)
async def create_blog(blog: Blog):
    return {'data': f"Blog is created with title as {blog.title}"}




# @app.get('/blog')
# def index(limit=10, published: bool = True, sort: Optional[str] = None):
#     # only get 10 published blogs
#     if published:
#         return {'data': f'{limit} published blogs from the db'}
#     else:
#         return {'data': f'{limit} blogs from the db'}
# workon blog
# uvicorn main:app --reload