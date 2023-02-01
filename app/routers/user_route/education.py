import hashlib
import smtplib
from random import randbytes
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter, Request

from ... import utils, oauth2
from app.models import user_model, models
from ...database import get_db, engine
from sqlalchemy.orm import Session
from app.email import Email
from app.schemas.user_schemas import education_schema

router = APIRouter(
    prefix='/users',
    tags=['Users Education']
)


# ! Get Education Details
@router.get('/education/{profileId}')
async def get_user_educations(profileId: int, db: Session = Depends(get_db)):

    query_education = db.query(user_model.Education).filter(
        user_model.Education.userProfileId == profileId).order_by(user_model.Education.id).all()

    # if not query_education:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Data does not exist")

    return query_education


# ! Create Education
@router.post('/education/', status_code=status.HTTP_201_CREATED)
async def add_education(body: education_schema.CreateEducation, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):

    query_user = db.query(models.UserProfile).filter(models.UserProfile.profileId ==
                                                     current_user.id).first()

    if not query_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden Request")

    new_education = user_model.Education(
        userProfileId=query_user.id, **body.dict())

    db.add(new_education)
    db.commit()
    db.refresh(new_education)

    return new_education


#! Update Education
@router.patch('/education/{id}', status_code=status.HTTP_200_OK)
async def update_education(id: int, body: education_schema.UpdateEducation, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    query_userProfile = db.query(models.UserProfile).filter(
        models.UserProfile.profileId == current_user.id)
    userProfile = query_userProfile.first()

    if not userProfile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User profile Does not exist!!!')

    print("Current User Id => " + str(current_user.id))
    print("User Profile Id => " + str(userProfile.id))

    query_skills = db.query(user_model.Education).filter(
        user_model.Education.id == id)

    skill = query_skills.first()

    if skill == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No data found with id: {id}')

    print("Skill Profile id => "+str(skill.userProfileId))

    if skill.userProfileId != userProfile.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f'Forbidden Request!!!')

    query_skills.update(body.dict(exclude_unset=True),
                        synchronize_session=False)

    db.commit()
    db.refresh(skill)

    return skill


#! Delete Education
@router.delete('/education/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_education(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    query_userProfile = db.query(models.UserProfile).filter(
        models.UserProfile.profileId == current_user.id)
    userProfile = query_userProfile.first()

    if not userProfile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User profile Does not exist!!!')

    print("Current User Id => " + str(current_user.id))
    print("User Profile Id => " + str(userProfile.id))

    query_skills = db.query(user_model.Education).filter(
        user_model.Education.id == id)

    skill = query_skills.first()

    if skill == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No data found with id: {id}')

    print("Skill Profile id => "+str(skill.userProfileId))

    if skill.userProfileId != userProfile.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f'Forbidden Request!!!')

    query_skills.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
