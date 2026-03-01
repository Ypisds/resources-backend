from dataclasses import dataclass
from ..infra.database import get_session
from typing import Annotated
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from ..models.user import User, UserRequest
from pwdlib import PasswordHash

encoder = PasswordHash.recommended()

def verify_password(plain_password: str, hashed_password: str):
    return encoder.verify(plain_password, hashed_password)

def get_password_hash(plain_password):
    return encoder.hash(plain_password)

@dataclass
class UserService():
    db: Annotated[Session, Depends(get_session)]

    def create_user(self, user_request: UserRequest):
        statement = select(User).where(
            User.username == user_request.username
        )
        result = self.db.exec(statement).first()

        if result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Usuário já existe"
            )
        
        hashed_password = get_password_hash(user_request.password)
        new_user = User(name=user_request.name, username=user_request.username, password=hashed_password)

        self.db.add(new_user)
        self.db.commit()
    
    def get_user(self, username: str) -> User:
        statement = select(User).where(
            User.username == username
        )
        user_returned = self.db.exec(statement).first()

        if not user_returned:
            return False

        return user_returned
    
    def authenticate_user(self, username: str, password: str) -> User:
        user_returned = self.get_user(username=username)
        
        if not user_returned:
            return False

        if not verify_password(password, user_returned.password):
            return False
        
        return user_returned


            


