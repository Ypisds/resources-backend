from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, status, Depends, Response
from typing import Annotated
from datetime import datetime, timezone, timedelta
from ..models.user import UserRequest

import jwt
from ..dependencies import get_user_service
from pydantic import BaseModel
from .config import settings
from jwt import InvalidTokenError
from ..services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

class Token(BaseModel):
    access_token: str
    token_type: str        

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_service: Annotated[UserService, Depends(get_user_service)]):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    user = user_service.get_user(username)
    if not user:
        raise credentials_exception
    return user

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> Token:
    user = user_service.authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.username}
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post("/create-user")
async def create_user(user: UserRequest, service: Annotated[UserService, Depends(get_user_service)]):
    service.create_user(user_request=user)
    return Response(status_code=status.HTTP_201_CREATED)


