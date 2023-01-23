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
from app.schemas.user_schemas import projects_schema

router = APIRouter(
    prefix='/users',
    tags=['Users Projects']
)


# ! Get Projects Details
@router.get('/project/{profileId}')
async def get_user_project(profileId: int, db: Session = Depends(get_db)):

    query_project = db.query(user_model.Projects).filter(
        user_model.Projects.userProfileId == profileId).order_by(user_model.Projects.id).all()

    if not query_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Data does not exist")

    return query_project


# ! Create Projects
@router.post('/project/', status_code=status.HTTP_201_CREATED)
async def add_project(body: projects_schema.CreateProject, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):

    query_user = db.query(models.UserProfile).filter(models.UserProfile.profileId ==
                                                     current_user.id).first()

    if not query_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden Request")

    new_project = user_model.Projects(
        userProfileId=query_user.id, **body.dict())

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


#! Update Projects
@router.patch('/project/{id}', status_code=status.HTTP_200_OK)
async def update_project(id: int, body: projects_schema.CreateProject, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    query_userProfile = db.query(models.UserProfile).filter(
        models.UserProfile.profileId == current_user.id)
    userProfile = query_userProfile.first()

    if not userProfile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User profile Does not exist!!!')

    print("Current User Id => " + str(current_user.id))
    print("User Profile Id => " + str(userProfile.id))

    query_skills = db.query(user_model.Projects).filter(
        user_model.Projects.id == id)

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


#! Delete Projects
@router.delete('/project/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    query_userProfile = db.query(models.UserProfile).filter(
        models.UserProfile.profileId == current_user.id)
    userProfile = query_userProfile.first()

    if not userProfile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User profile Does not exist!!!')

    print("Current User Id => " + str(current_user.id))
    print("User Profile Id => " + str(userProfile.id))

    query_skills = db.query(user_model.Projects).filter(
        user_model.Projects.id == id)

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
