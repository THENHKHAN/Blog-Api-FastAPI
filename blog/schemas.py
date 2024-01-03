from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


# for validation and conversion : Pydantic
class BlogPydantic(BaseModel):
    title: str
    description: str
    # published: Optional[bool] = False  or without bool = False will work the same
    created_at: Optional[str] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# one way:
class Show(BaseModel): 
    #  only returning title and description # whatver attribute wa want to send response we can define here
     title: str
     description: str
    #  id : int
     model_config = ConfigDict(from_attributes=True) 


# Other way: # returning as per the BlogPydantic
# class Show(BlogPydantic):  
#    # means Blog class (DB table will return ap per the BlogPydantic shcema )
#     model_config = ConfigDict(from_attributes=True) 
#     # class Config: # earlier it was  Config()
    # class Config: #also working
    #     from_attributes = True  
# Earlier it was :
'''
class Show(BlogPydantic): 

    class Config():
        orm_mode = True
'''


# Use Pydantic's orm_mode : https://fastapi.tiangolo.com/tutorial/sql-databases/    scroll and get the doc with this heading why we are using : https://www.youtube.com/watch?v=7t2alSnE2-I&t=164s

