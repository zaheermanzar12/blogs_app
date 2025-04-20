import json

from fastapi import HTTPException
from typing import Optional, List
from fastapi import Query

from blogs.configs.redis_client import get_redis
from blogs.db.database import database
from blogs.models.blogs import BlogsResponse, BlogDetails


async def create_new_blog(name: str, description: str, blog_type: Optional[str] = Query(default=None)) -> str:
    """
    Add new blog data in database
    """
    if not blog_type:
        blog_type = 'informative'
    await database.execute(
        """
    INSERT INTO public.blogs (name, description, blog_type)
    VALUES (:name, :description, :blog_type)
    """,
    values={
        "name": name,
        "description": description,
        "blog_type": blog_type
    })
    return "Blog Created Successfully"


async def update_blog(
        blog_id: int,
        name: Optional[str] = Query(default=None),
        description: Optional[str] = Query(default=None),
        blog_type: Optional[str] = Query(default=None),
        is_active: Optional[bool] = Query(default=None)
) -> str:
    """
    Update blog info on base of Blog Id
    """
    blog_data =  await database.fetch_one(
        """
            select id, name, blog_type, description
            from blogs 
            where id=:blog_id and is_deleted = :is_deleted;
        """,
        {"blog_id":blog_id, "is_deleted": False}
    )
    if not blog_data:
        raise HTTPException(status_code=404, detail="Invalid blog ID")
    if not name:
        name = blog_data.name
    if not description:
        description = blog_data.description
    if not blog_type:
        blog_type = blog_data.blog_type

    await database.execute(
        """
        UPDATE blogs
        SET
            name = :name,
            description = :description,
            blog_type = :blog_type,
            is_active = :is_active
        WHERE id = :id
        """,
        values={
            "id": blog_id,
            "name": name,
            "description": description,
            "blog_type": blog_type,
            "is_active": is_active  # Pass False to deactivate
        }
    )
    return "Blog Updated Successfully"


async def get_blog_details(blog_id) -> BlogDetails:
    """
    Get details of blog base on Blog ID
    """
    blog = await database.fetch_one(
        """
            select id, name, blog_type, description, is_active, Date(created_at) as created_at
            from blogs 
            where id=:blog_id and is_active = :is_active and is_deleted = :is_deleted;
        """,
        {"blog_id":blog_id, "is_active": True, "is_deleted": False}
    )
    if not blog:
        raise HTTPException(status_code=404, detail="Invalid blog ID")
    return BlogDetails(**blog)


async def get_blogs() -> List[BlogsResponse]:
    """
    Get all active blogs in system
    """
    redis = await get_redis()
    cache_key = "active_blogs"

    cached_data = await redis.get(cache_key)
    if cached_data:
        print("FOUND IN CACHE")
        blogs = json.loads(cached_data)
        return [BlogsResponse(**blog) for blog in blogs]

    blogs = await database.fetch_all(
        """
        select id, name, blog_type from blogs where is_active = :is_active and is_deleted = :is_deleted;
        """,
        {"is_active": True, "is_deleted": False}
    )
    blogs_list = [BlogsResponse(**blog) for blog in blogs]
    print("SETTING CACHE")
    await redis.set(cache_key, json.dumps([b.dict() for b in blogs_list]), ex=60)

    return blogs_list


async def delete_blog_by_id(blog_id: int) -> str:
    """
    Delete a blog on base of id
    """
    get_blog_info = await database.fetch_one(
        """
        Select id from blogs where id = :blog_id;
        """,
        {"blog_id": blog_id}
    )
    if not get_blog_info:
        raise HTTPException(status_code=404, detail="Invalid blog ID")
    await database.execute(
        """
        UPDATE blogs
        SET
            is_deleted = :is_deleted
            WHERE id = :id
            """,
            values={
                "id": blog_id,
                "is_deleted": True
            }
    )
    return "Blog Deleted Successfully"