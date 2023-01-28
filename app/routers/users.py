import hashlib
import smtplib
from random import randbytes
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter, Request
from .. import utils, oauth2
from app.models import models
from app.schemas import schemas, user_profile_schema
from ..database import get_db, engine
from sqlalchemy.orm import Session
from app.email import Email

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(request: Request, user: schemas.CreateUser, db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(
        models.User.email == user.email)

    user_exist = user_query.first()

    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with {user.email} already exist")

    # password hashing
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    try:
        token = randbytes(10)
        hashedCode = hashlib.sha256()
        hashedCode.update(token)
        verification_code = hashedCode.hexdigest()
        print(verification_code)

        user_query.update({'otpCode': verification_code},
                          synchronize_session=False)
        db.commit()

        # url = f"{request.url.scheme}://{request.client.host}:{request.url.port}/verifyemail/{token.hex()}" # uncomment after domain integration
        url = f"{request.url.scheme}://15.207.116.185/verifyemail/{token.hex()}"
        print(url)

        await Email(new_user, url, [user.email]).sendVerificationCode()

    except Exception as error:
        print('Error', error)
        user_query.update({'otpCode': None}, synchronize_session=False)
        db.commit()

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='There was an error sending email')

    return {'status': 'success', 'message': 'Verification token successfully sent to your email'}


@router.patch('/profile-type', status_code=status.HTTP_200_OK)
def update_user_profile_type(user: schemas.UserProfileType, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    user_query = db.query(models.User).filter(
        models.User.id == current_user.id)

    user_found = user_query.first()

    print(user_query)
    print(user)
    print(user_found)

    if user_found.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Forbidden Request")

    user_query.update(user.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    db.refresh(user_found)

    return {"detail": "Successfully updated"}


@router.get('/me')
def get_profile(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):
    user = db.query(models.User).filter(models.User.id ==
                                        current_user.id).all()  # For same user posts only

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Data does not exist")
    print(user)
    return user


@router.get('/{id}')
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Data does not exist with {id}")
    return user


# ----------------------------------------------------------- Candidate Profile  ------------------------------------------------------------- #
# ----------------------------------------------------------- Candidate Profile  ------------------------------------------------------------- #
# ----------------------------------------------------------- Candidate Profile  ------------------------------------------------------------- #


@router.post('/profile', status_code=status.HTTP_201_CREATED)
async def create_user_profile(request: Request, body: user_profile_schema.CreateUserProfile, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):

    if current_user.profileType != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Allowed!!!")

    query_userProfile = db.query(models.UserProfile).filter(
        models.UserProfile.profileId == current_user.id).first()

    if query_userProfile:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'User already exist')

    user_profile = models.UserProfile(profileId=current_user.id, **body.dict())

    db.add(user_profile)
    db.commit()
    db.refresh(user_profile)

    return user_profile


@router.patch('/profile', status_code=status.HTTP_200_OK, response_model=user_profile_schema.ResponseUserProfile)
async def update_user_profile(body: user_profile_schema.UpdateUserProfile, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    query_userProfile = db.query(models.UserProfile).filter(
        models.UserProfile.profileId == current_user.id)
    userProfile = query_userProfile.first()

    if not userProfile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User profile Does not exist!!!')

    query_userProfile.update(body.dict(exclude_unset=True),
                             synchronize_session=False)
    db.commit()

    return userProfile


@router.get('/profile/me', response_model=user_profile_schema.ResponseUserProfile)
def get_user_profile(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):

    user = db.query(models.UserProfile).filter(models.UserProfile.profileId ==
                                               current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Data does not exist")
    print(user)
    return user


# TODO: soft skills CRUD
