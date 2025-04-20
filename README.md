
# 📝 FastAPI Blogs CRUD Application

A FastAPI-based application for managing blogs with secure JWT authentication, PostgreSQL database, Redis caching, and Docker support, including test cases using pytest.

---

## 🚀 Features

- ✅ Create, Read, Update, Delete (CRUD) for blogs
- 🔐 JWT-based user authentication using OAuth2
- 🧠 Redis cache for faster GET operations
- 🗃 PostgreSQL database integration using `databases` and `asyncpg`
- 🐳 Dockerized setup for easy deployment
- 📄 Interactive API docs via Swagger UI (`/docs`)
- 🧪 Built-in test cases using `pytest` to verify CRUD functionality and auth flows
---

# Project Configurations

Clone the code from github repo using.

git clone git@github.com:zaheermanzar12/blogs_app.git

1. Create or load postgres database with name blogs_db and update the settings file Parameters
2. Configure redis on your system and execute redis using 

1. [ ] sudo service redis-server start
2. [ ] redis-cli

**Test Redis**

127.0.0.1:6379> ping 
- PONG

# run below mentioned commands to setup code

1. [ ] `python -m venv venv
2. [ ] source venv/bin/activate  # On Windows: venv\Scripts\activate
3. [ ] pip install -r requirements.txt`

# Commands to execute APP and Test Cases

* uvicorn main:app --reload
* 
* pytest .\tests\blogs_test.py


# Link to open swagger API Docs.

* http://localhost:8000/blogs/docs#
