from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from fastapi.responses import JSONResponse

from .. import database, models, schemas
from .. import hashing 

router = APIRouter(
      prefix="/blog",
      tags=["Blogs"]

)
get_db = database.get_db


@router.get("/", status_code=200,response_model=Dict[str, List[schemas.ShowBlog]])
async def all(db:Session = Depends(get_db) ):
        try:
            blogs = db.query(models.Blog).all() # .all() give list of blogs
            print(blogs)
            print(type(blogs))
            print("---> ")
            # checking that every blog has associated with user id . checking And null or not
            flag = True
            for blog in blogs:
                 print(blog.user_id)
                 if blog.user_id == None:   
                    flag = False
                    break
            print(flag)
            if blogs == None or not flag : # will run either blogs is null or glag is false(user_di is null)         
                return JSONResponse(status_code=404, content={"message": "Data not found or user id is null"}) # In the key content, that has as value another JSON object (dict) that contains
            else:
                return {"data":blogs }
        except Exception as e :
           raise HTTPException(status_code=500, detail= str(e))


# get single blog post by id dynamically : Also handling HHPException with status code if post is not found of desired id
@router.get("/{id}" , status_code=200, response_model=schemas.ShowBlog) # we have controlled the response by response_model : Now this will return accoring to Show() schemas even we get id as well from db of Blog Class instance
async def show(id:int, db:Session = Depends(get_db)):
    try: 
        single_post = db.query(models.Blog).filter(id == models.Blog.id).first()
        print(single_post)# insatance of Blog model class : it will print  def __repr__(self) -> str:  return f"Id = {self.id}, title = {self.title})"
        if not single_post or single_post.user_id == None: # means if single_post== None
            raise HTTPException(status_code=404, detail={"message": f"Data not found of ID - {id} or user id is null"})  # HTTPException(status_code, detail=None, headers=None) OR raise HTTPException(status_code=404, detail="Item not found")
            # https://fastapi.tiangolo.com/reference/exceptions/?h=htt
        else:
            return single_post
    except Exception as e :
           raise HTTPException(status_code=500, detail= str(e))        



@router.post("/", status_code=201, response_model=Dict[str,str|dict])
async def create(request:schemas.BlogPydantic, db:Session = Depends(get_db)): # created an instance of Session that will work as a connection and db will be the variable for this . Everything will be done through db variable related to database.
     try:
            new_blog = models.Blog(title = request.title , description = request.description, created_at = request.created_at, user_id=1 ) # creating instance of model Blog class here to isert data and mapped with db and class
            db.add(new_blog)
            db.commit()
            db.refresh(new_blog)
            return {"status": "blog created successfully" ,"blog_detail": {"title":new_blog.title, "desc":new_blog.description}} 
     
     except Exception as e:
    # By this way we can know about the type of error occurring
        print("The error is: ",e)
        return {"status_code":404, "detail": f"Blog not created - error is {e}"  }
        # return JSONResponse(status_code=404, content= {"error" : "Blog cannot be created", "errorDetail" : f"The error is: {e}", }) also working



# get delete blog post by id dynamically :
@router.delete("/{id}", status_code=200)
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
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
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


