from typing import Any

from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session 

from blogapp import schemes, models
from blogapp.database import get_session

 
class BaseService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_model_by(self, model: models.BaseModel,  params: dict) -> Any:
        data_object = (
            self.session
            .query(model)
            .filter_by(**params)
            .first()
        )
        if not data_object:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The entry not found"
            )
        return data_object

    def _verify_credential(self, entry_owner_id: int, token_data: schemes.TokenData):
        permission_exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only author have permission to change it"
        )
        token_owner_data = self._get_model_by(models.User, {'username' : token_data.username})
        if entry_owner_id != token_owner_data.id:
            raise permission_exception

