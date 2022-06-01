from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from blogapp import schemes
from blogapp.settings import settings
from blogapp.services.auth import AuthService, oauth_scheme


router = APIRouter(prefix='/auth', tags=["auth"])


@router.post("/sign-up/", response_model=schemes.Token)
async def sign_up(
    user: schemes.UserCreate,
    service: AuthService = Depends()
):
    return service.register_new_user(user)


@router.post("/sign-in/", response_model=schemes.Token)
async def sign_in(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends()
):
    return service.athenticate_user(form_data.username, form_data.password)


@router.get("/users/me/", response_model=schemes.UserInDB)
async def read_users_me(
    token: str = Depends(oauth_scheme),
    service: AuthService = Depends()
):
    return service.get_current_user(token)
