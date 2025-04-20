from blogs.db.database import database


async def verify_user_exists(username: str) -> bool:
    user_info = await database.fetch_one(
        """
        select id from users where username = :username;
        """,
        {"username": username}
    )
    print(user_info)
    if user_info:
        return True
    else:
        return False


async def create_user(username:str, password: str):
    await database.execute(
        """
        INSERT
        INTO
        users(username, password_hash, is_active)
        VALUES(:username, :password, :is_active)
        """,
        values={
        "username": username,
        "password": password,
        "is_active": True
        }
    )
    return True


async def verify_user_by_name_password(username: str, password: str) -> bool:
    user_info = await database.fetch_one(
        """
        select id from users where username = :username and password = :password;
        """,
        {"username": username, "password": password}
    )
    if user_info:
        return True
    else:
        return False
