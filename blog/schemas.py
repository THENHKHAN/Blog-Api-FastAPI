from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


# for validation and conversion : Pydantic
class BlogPydantic(BaseModel):
    title: str
    description: str
    # published: Optional[bool] = False  or without bool = False will work the same
    created_at: Optional[str] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


class Show(BaseModel):
    data: BlogPydantic # means Blog class (DB table will return ap per the BlogPydantic shcema )

    # class Config: # earlier it was  Config()
    model_config = ConfigDict(from_attributes=True) 
    # class Config: #also working
    #     from_attributes = True  
# Earlier it was :
'''
class Show(BlogPydantic): 

    class Config():
        orm_mode = True
'''


# Use Pydantic's orm_mode : https://fastapi.tiangolo.com/tutorial/sql-databases/    scroll and get the doc with this heading why we are using : https://www.youtube.com/watch?v=7t2alSnE2-I&t=164s

