import random

import pytest
from httpx import AsyncClient
from fastapi import status

from blogs.configs.security import create_access_token
from main import app

# A valid JWT token (replace with dynamically generated token in real case)
token = create_access_token({"sub": "admin"})
FAKE_JWT = f'Bearer {token}'

@pytest.mark.asyncio
async def test_get_user_token():
    async with AsyncClient(base_url="http://localhost:8000/blogs") as ac:
        response = await ac.post(
            "/auth/login", data={"username": "admin", "password": "admin123"}
        )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)


@pytest.mark.asyncio
async def test_get_all_blogs():
    async with AsyncClient(base_url="http://localhost:8000/blogs") as ac:
        response = await ac.get("/blogs", headers={"Authorization": FAKE_JWT})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_blog_by_id():
    async with AsyncClient(base_url="http://localhost:8000/blogs") as ac:
        response = await ac.get("/blogs/1", headers={"Authorization": FAKE_JWT})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)


@pytest.mark.asyncio
async def test_create_blog():
    random_number = random.randint(1000, 9999)
    # blog_data = "name=Test Blog&description=This is a test blog&blog_type=Informative"
    async with AsyncClient(base_url="http://localhost:8000/blogs") as ac:
        response = await ac.post(f"/blogs/add_blog?name=new_blog{random_number}&description=its_done", headers={"Authorization": FAKE_JWT})
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]


@pytest.mark.asyncio
async def test_update_blog():
    blog_id = 1  # Replace with actual blog ID from your DB
    update_data = {
        "name": "Updated Blog",
        "description": "Updated description",
        "blog_type": "News"
    }
    async with AsyncClient(base_url="http://localhost:8000/blogs") as ac:
        response = await ac.put(f"/blogs/update_blog?blog_id={blog_id}", json=update_data, headers={"Authorization": FAKE_JWT})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete_blog():
    blog_id = 4
    async with AsyncClient(base_url="http://localhost:8000/blogs") as ac:
        response = await ac.delete(f"/blogs/delete_blog?blog_id={blog_id}", headers={"Authorization": FAKE_JWT})
    assert response.status_code == status.HTTP_200_OK
