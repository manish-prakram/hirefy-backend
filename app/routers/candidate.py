import hashlib
import smtplib
from random import randbytes
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter, Request
from .. import utils, oauth2
from app.models import models
from app.schemas import schemas, user_profile_schema
from app.schemas.user_schemas import user_schema
from ..database import get_db, engine
from sqlalchemy.orm import Session
from app.email import Email

router = APIRouter(
    prefix='/candidate',
    tags=['Candidate']
)
# ----------------------------------------------------------- Candidate Profile  ------------------------------------------------------------- #
# ----------------------------------------------------------- Candidate Profile  ------------------------------------------------------------- #
# ----------------------------------------------------------- Candidate Profile  ------------------------------------------------------------- #


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user_profile(request: Request, body: user_profile_schema.CreateUserProfile, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):

    if current_user.profileType != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Allowed!!!")

    query_userProfile = db.query(models.UserProfile).filter(
        models.UserProfile.profileId == current_user.id).first()

    if query_userProfile:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Candidate already exist')

    user_profile = models.UserProfile(profileId=current_user.id, **body.dict())

    db.add(user_profile)
    db.commit()
    db.refresh(user_profile)

    return user_profile


@router.patch('/', status_code=status.HTTP_200_OK, response_model=user_profile_schema.ResponseUserProfile)
async def update_user_profile(body: user_profile_schema.UpdateUserProfile, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    query_userProfile = db.query(models.UserProfile).filter(
        models.UserProfile.profileId == current_user.id)
    userProfile = query_userProfile.first()

    if not userProfile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Candidate profile Does not exist!!!')

    query_userProfile.update(body.dict(exclude_unset=True),
                             synchronize_session=False)
    db.commit()

    return userProfile


@router.get('/me')
def get_user_profile(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):

    user = db.query(models.UserProfile).filter(models.UserProfile.profileId ==
                                               current_user.id).first()
    if not user:
        return {
            'status_code': 404,
            'message': 'Candidate not created yet',
            'data': []
        }
        
    print(user)
    return user


@router.get('/{id}', response_model=user_profile_schema.ResponseUserProfile)
def get_user_profile(id: int, db: Session = Depends(get_db),):

    user = db.query(models.UserProfile).filter(models.UserProfile.profileId ==
                                               id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Candidate details with id: {id} not found")
    print(user)
    return user
