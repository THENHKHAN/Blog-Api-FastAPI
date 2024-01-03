from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException,Response, status
from fastapi.responses import JSONResponse
# importing desired dependecy from other files
from blog.database import SessionLocal, engine #blog.database we have to provide project directgory/ package (that's y init inside the blog directory)
from sqlalchemy.orm import Session
from typing import List, Dict

from . import models # # from database model
from . import schemas # from pydantic model
from .hashing import Hash

models.Base.metadata.create_all(bind=engine) # migrating all the changes. If table is not there then create a new one and if there then it wont  create 

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # here we are closing


@app.get("/" , tags=["blogs"])
async def index ():
       return {"message": "Hello World!"}

@app.post("/blog/", status_code=20, tags=["blogs"])
async def create(request:schemas.BlogPydantic, db:Session = Depends(get_db)): # created an instance of Session that will work as a connection and db will be the variable for this . Everything will be done through db variable related to database.
     try:
            new_blog = models.Blog(title = request.title , description = request.description, created_at = request.created_at) # creating instance of model Blog class here to isert data and mapped with db and class
            db.add(new_blog)
            db.commit()
            db.refresh(new_blog)
            return {"data" : {"status":"blog created successfully" ,"body":new_blog} }
     
     except Exception as e:
    # By this way we can know about the type of error occurring
        print("The error is: ",e)
        return {"status_code":404, "error":[ {"detail": "Blog not created"} , {"errorDetail" : f"The error is: {e}"} ] }
        # return JSONResponse(status_code=404, content= {"error" : "Blog cannot be created", "errorDetail" : f"The error is: {e}", }) also working

@app.get("/blog/", status_code=200, tags=["blogs"])
async def all(db:Session = Depends(get_db)):
        blogs = db.query(models.Blog).all() # .all() give list of blogs
        print(blogs)
        if blogs == None:           
            return JSONResponse(status_code=404, content={"message": "Data not found"}) # In the key content, that has as value another JSON object (dict) that contains
        else:
            return {"data":blogs }

# get all the blogs under a particular tables
@app.get("/blog/byResponse_model", status_code=200, response_model=Dict[str, List[schemas.Show]], tags=["blogs"])
async def all2(db:Session = Depends(get_db)):
        blogs = db.query(models.Blog).all() # .all() give list of blogs
        print(blogs)
        if blogs == None:           
            return JSONResponse(status_code=404, content={"message": "Data not found"}) # In the key content, that has as value another JSON object (dict) that contains
        else:
            return {"data":blogs } # blogs if it is a single record then it will return single record in the form of object(dict)/json but if it has multiple records then it will rturn as list of records in the form of JSON , FastAPI will take of these
        '''
                            {
                    "data": [
                        {
                        "description": "string1",
                        "title": "string1",
                        "created_at": "02/01/2024 19:38:13",
                        "id": 1
                        }
                    ]
                    }

                    for multiple :
                        {
                            "data": [
                                {
                                "title": "string1",
                                "created_at": "02/01/2024 19:38:13",
                                "description": "string1",
                                "id": 1
                                },
                                {
                                "title": "string333",
                                "created_at": "02/01/2024 21:28:32",
                                "description": "strin33g",
                                "id": 2
                                }
                            ]
                        }
        '''

# get single blog post by id dynamically : Also handling HHPException with status code if post is not found of desired id
@app.get("/blog/{id}" , status_code=200, response_model=schemas.Show, tags=["blogs"]) # we have controlled the response by response_model : Now this will return accoring to Show() schemas even we get id as well from db of Blog Class instance
async def show(id:int, db:Session = Depends(get_db)):
    try: 
        single_post = db.query(models.Blog).filter(id == models.Blog.id).first()
        print(single_post)# insatance of Blog model class : it will print  def __repr__(self) -> str:  return f"Id = {self.id}, title = {self.title})"
        if not single_post : # means if single_post== None
            raise HTTPException(status_code=404, detail={"message": f"Data not found of ID - {id}"})  # HTTPException(status_code, detail=None, headers=None) OR raise HTTPException(status_code=404, detail="Item not found")
            # https://fastapi.tiangolo.com/reference/exceptions/?h=htt
        else:
            return single_post
    except Exception as e :
           raise HTTPException(status_code=500, detail= str(e))        



# get delete blog post by id dynamically :
@app.delete("/blog/{id}", status_code=200, tags=["blogs"])
async def delete(id:int, db: Session = Depends(get_db)):
        single_post = db.query(models.Blog).filter(id == models.Blog.id).first() # getting the record of desired blog id 
        
        print(single_post)
        if single_post == None:                      
            return JSONResponse(status_code=404, content={"message": f"Data not found of ID - {id}"}) # In the key content, that has as value another JSON object (dict) that contains
        else:
            db.delete(single_post) # this object/rocord will be deleted 
            db.commit()
            # blog = db.query(models.Blog).all()
            return {"status" : f"Blog of id: {id} deleted successfully"} 
            # return {"status" : f"Blog of id: {id} deleted successfully" , "remainingBlog" : blog} 


#  for update
@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
async def update(id:int, request: schemas.BlogPydantic,  db: Session = Depends(get_db)):
        try:
            blog = db.query(models.Blog).filter(id == models.Blog.id).first()     
            if blog == None:                      
                raise HTTPException(status_code=404, detail={"message": f"Data not found of ID - {id}"})
            else:
                blog = db.query(models.Blog).filter(id == models.Blog.id).update({"title": request.title, "description":request.description})        
                # blog = db.query(models.Blog).filter(id == models.Blog.id).update({"title": request.title, "description":request.description}, synchronize_session='evaluate')  also work       
                db.commit()
                return {"status" : f"Blog of id: {id} Updated successfully"}
        except Exception as e :
                raise HTTPException(status_code=500, detail= str(e)) # str(e) since e alone is type of Exception which is not serializable hence cast into string so that we can sent it as error msg


# https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update
    #    Below is also anotherway to do the same thing
        '''
        try:
            # Retrieve the blog to update
            blog = db.query(models.Blog).filter(models.Blog.id == id).first()

            # Check if the blog with the specified id exists
            if blog is None:
                raise HTTPException(status_code=404, detail="Blog not found")

            # Update the blog attributes
            blog.title = request.title
            blog.description = request.description

            # Commit the changes to the database
            db.commit()

            return {"status": "Blog updated successfully"}

        except Exception as e:
            print("The error is:", e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        '''


#  FOR USER Stuff

# for creating user : means post request
@app.post("/user/", status_code=201, response_model=Dict[str, schemas.ShowUser|str], tags=["users"])
async def create_user(request: schemas.UserPydantic, db:Session = Depends(get_db)):
    try:
        
        new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password), created_at = request.created_at)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"status": "User created successfully", "user_detail": new_user}
    
    except Exception as e :
        print("The error is: ",e)
        return {"status_code":404, "error":[ {"detail": "USER not created"} , {"errorDetail" : f"The error is: {e}"} ] }
        # return JSONResponse(status_code=404, content= {"error" : "Blog cannot be created", "errorDetail" : f"The error is: {e}", }) also working


@app.get("/user/", status_code=200, response_model=List[schemas.ShowUser]|Dict[str,str], tags=["users"])
async def show_users(db:Session = Depends(get_db)):
     users = db.query(models.User).all()
     print(users)
     if users == None or users == []:           
        return JSONResponse(status_code=404, content={"message": "No user exist"}) # In the key content, that has as value another JSON object (dict) that contains
     else:
            # return {"data":blogs }
            return users

@app.get("/user/{id}", status_code=200, response_model=schemas.ShowUser|Dict[str,str], tags=["users"])
async def show_user(id:int, db:Session = Depends(get_db)):
     try:
        user = db.query(models.User).filter(id == models.User.id).first()
        print(user)
        if user == None or user == []: 
            raise HTTPException(status_code=404, detail={"message": f"User of Id : {id} Not exist" })  
        else:
                return user        
     except Exception as e: 
                print("error : ", e)
                raise HTTPException(status_code=500, detail= str(e))
          

#Run server:(blog) E:\NHKHAN_studySelf\1-ColabsWithTHE_NHKHAN\BitFumesFastAPi>uvicorn blog.main:app 