from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
# importing desired dependecy from other files
from blog.database import  engine #blog.database we have to provide project directgory/ package (that's y init inside the blog directory)
from sqlalchemy.orm import Session
from typing import List, Dict, Union

from . import models # # from database model
from . import schemas # from pydantic model
from .routers import blogs, users #routers is the direciry and blog is the blog.py 
from .database import get_db


models.Base.metadata.create_all(bind=engine) # migrating all the changes. If table is not there then create a new one and if there then it wont  create 

app = FastAPI()

# Configure CORS
origins = ["*"]  # Update this to the specific origins of your frontend

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(blogs.router) # router- instantiated from blog.py inside blog.py
app.include_router(users.router) # router- instantiated from blog.py inside blog.py

#  below these two routes are just for testing purpose f main.py
@app.get("/" , tags=["In_main"])
async def index ():
       return {"message": "Hello World!"}

# get all the blogs under a particular tables
@app.get("/blog/byResponse_model", status_code=200, response_model=Dict[str, List[schemas.ShowBlog]], tags=["In_main"])
async def all2(db:Session = Depends(get_db)):
        blogs = db.query(models.Blog).all() # .all() give list of blogs
        print(blogs)
        if blogs == None:           
            return JSONResponse(status_code=404, content={"message": "Data not found"}) # In the key content, that has as value another JSON object (dict) that contains
        else:
            return {"data":blogs } # blogs if it is a single record then it will return single record in the form of object(dict)/json but if it has multiple records then it will rturn as list of records in the form of JSON , FastAPI will take of these

#Run server:(blog) E:\NHKHAN_studySelf\1-ColabsWithTHE_NHKHAN\BitFumesFastAPi>uvicorn blog.main:app 