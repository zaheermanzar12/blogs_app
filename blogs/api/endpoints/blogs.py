from fastapi import Query

from blogs.configs.security import get_current_user
from blogs.db.blogs_queries import get_blog_details, update_blog, delete_blog_by_id, create_new_blog, get_blogs
from blogs.models.blogs import *
from typing import List, Optional
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/blogs")


@router.get("", name="Show All Blogs", response_model=List[BlogsResponse])
async def get_all_blogs(
    current_user: dict = Depends(get_current_user)
):
    blogs = await get_blogs()
    return blogs


@router.get("/{blog_id}", name="Get Blog Detail", response_model=BlogDetails)
async def get_blog_data(
    blog_id: int,
    current_user: dict = Depends(get_current_user)
):
    blogs = await get_blog_details(blog_id)
    return blogs


@router.post("/add_blog", name="Create New Blog")
async def create_blog(
    name: str,
    description: str,
    blog_type: Optional[str] = Query(default=None),
    current_user: dict = Depends(get_current_user)

) -> str:
    blog = await create_new_blog(name, description, blog_type)
    return blog


@router.delete("/delete_blog", name="Delete New Blog")
async def delete_blog_data(
    blog_id: int,
    current_user: dict = Depends(get_current_user)
) -> str:
    blog = await delete_blog_by_id(blog_id)
    return blog


@router.put("/update_blog", name="Update Blog By Id")
async def update_blog_info(
    blog_id: int,
    name: Optional[str] = Query(default=None),
    description: Optional[str] = Query(default=None),
    blog_type: Optional[str] = Query(default=None),
    is_active: Optional[bool] = Query(default=True),
    current_user: dict = Depends(get_current_user)
) -> str:
    blog = await update_blog(blog_id, name, description, blog_type, is_active)
    return blog
