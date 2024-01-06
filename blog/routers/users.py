from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from fastapi.responses import JSONResponse

from .. import database, models, schemas
from ..hashing import Hash 

router = APIRouter(
       prefix="/user",
      tags=["Users"]

)

get_db = database.get_db

#  FOR USER Stuff

# for creating user : means post request
@router.post("/", status_code=201, response_model=Dict[str, schemas.ShowUser|str])
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


@router.get("/", status_code=200, response_model=List[schemas.ShowUser]|Dict[str,str])
async def show_users(db:Session = Depends(get_db)):
     users = db.query(models.User).all()
     print(users)
     if users == None or users == []:           
        return JSONResponse(status_code=404, content={"message": "No user exist"}) # In the key content, that has as value another JSON object (dict) that contains
     else:
            # return {"data":blogs }
            return users

@router.get("/{id}", status_code=200, response_model=schemas.ShowUser|Dict[str,str])
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
          
