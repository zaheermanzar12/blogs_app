from sqlite3 import Date

from pydantic import BaseModel, Field


class BlogDetails(BaseModel):
    id: int = Field(description="Blog Primary Id")
    name: str = Field(description="Name of Blog Posted")
    blog_type: str = Field(description="Type of Blog")
    description: str = Field(description="Content of Blog")
    is_active: bool = Field(description="Status of blog")
    created_at: Date = Field(description="Created time of Blog")


class BlogsResponse(BaseModel):
    id: int = Field(description="Blog primary Id")
    name: str = Field(description="Name of Blog Posted")
    blog_type: str = Field(description="Type of Blog")
