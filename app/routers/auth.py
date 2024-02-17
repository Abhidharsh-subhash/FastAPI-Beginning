from fastapi import Depends, status, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['authentication'])


@router.post('/login')
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # now here the data will only have two values that is username(email) and password
    user = db.query(models.User).filter_by(email=data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    elif not utils.verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    else:
        access_token = oauth2.create_access_token(data={'user_id': user.id})
        return {"msg": "successfully logged in", "access_token": access_token, "token_type": "bearer"}
