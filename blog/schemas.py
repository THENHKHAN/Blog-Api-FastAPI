from datetime import datetime
from pydantic import BaseModel
from typing import Optional


# for validation and conversion : Pydantic
class BlogPydantic(BaseModel):
    title: str
    descritpion: str
    # published: Optional[bool] = False  or without bool = False will work the same
    created_at: Optional[str] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")