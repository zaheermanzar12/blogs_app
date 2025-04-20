from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm

from blogs.configs.security import create_access_token, get_password_hash
from blogs.db.auth import verify_user_exists, create_user, verify_user_by_name_password
from blogs.models.auth import Token

router = APIRouter(prefix="/auth")


@router.post("/register")
def register(username: str, password: str):
    user_found = verify_user_exists(username)
    if user_found:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = get_password_hash(password)
    create_user(username, hashed)
    return {"msg": "User registered successfully"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = verify_user_by_name_password(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

