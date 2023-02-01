import hashlib
from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from .. import utils, oauth2
from app.models import models
from app.schemas import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_creds.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials!")

    if not utils.verify_password(user_creds.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials!!!!!")

    if user.emailVerified == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not verified!!! 😔")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {
        "email": user.email,
        "access_token": access_token,
        "token_type": "Bearer",
        "data": user,
    }


@router.get('/verifyemail/{token}')
def verify_me(token: str, db: Session = Depends(get_db)):
    hashedCode = hashlib.sha256()
    hashedCode.update(bytes.fromhex(token))
    verification_code = hashedCode.hexdigest()

    user_query = db.query(models.User).filter(
        models.User.otpCode == verification_code)
    user = user_query.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid verification code or user does not exist')

    if user.emailVerified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Email already verified')

    user_query.update({'emailVerified': True, 'otpCode': None},
                      synchronize_session=False)
    db.commit()

    return {
        "status": "success",
        "message": "Account verified successfully"
    }
