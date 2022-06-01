from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext

from blogapp import schemes, models
from blogapp.settings import settings
from blogapp.services.base import BaseService


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in/')


def get_current_user(token: str = Depends(oauth_scheme)) -> schemes.TokenData:
    return AuthService.verify_access_token(token)


class AuthService(BaseService):
    @classmethod
    def hash_password(cls, password: str) -> str:
        return pwd_context.hash(password)
    
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def verify_access_token(cls, token: str) -> schemes.TokenData:
        credentials_exception = HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
        try:
            paload = jwt.decode(token, settings.jwt_secret_key, algorithms=settings.jwt_algoritm)
        except JWTError:
            raise credentials_exception

        username: str = paload.get('sub')
        if username is None:
            raise credentials_exception

        token_data = schemes.TokenData(username=username)
        return token_data

    
    @classmethod
    def create_access_token(cls, user: models.User, expires_delta: Optional[timedelta] = None) -> schemes.Token:
        user_data = schemes.UserInDB.from_orm(user)
        now = datetime.utcnow()
        if expires_delta:
            expire = now + expires_delta
        else:
            expire = now + timedelta(minutes=15)
        paload = {
            'iat': now,
            'nbf': now,
            'exp': expire,
            'sub': user_data.username
        }
        encoded_jwt = jwt.encode(paload, settings.jwt_secret_key, settings.jwt_algoritm)
        return schemes.Token(
            access_token=encoded_jwt,
            token_type = "bearer"
        )
   
    def register_new_user(self, user: schemes.UserCreate) -> schemes.Token:
        user = models.User(
            username=user.username,
            email=user.email,
            password_hash=self.hash_password(user.plain_password)
        )
        self.session.add(user)
        self.session.commit()
        return self.create_access_token(user)
    
    def athenticate_user(self, username: str, plain_password: str) -> schemes.Token:
        print("start auhtentication")
        credentials_exception = HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
        user = (
            self.session
            .query(models.User)
            .filter_by(username=username)
            .first()
        )

        if not user:
            raise credentials_exception
        if not self.verify_password(plain_password, user.password_hash):
            raise credentials_exception
        
        return self.create_access_token(user)
    
    def get_current_user(self, token: str) -> models.User:
        credentials_exception = HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
        token_data = self.verify_access_token(token)
        
        user = (
            self.session
            .query(models.User)
            .filter_by(username=token_data.username)
            .first()
        )
        if not user:
            raise credentials_exception
        return user