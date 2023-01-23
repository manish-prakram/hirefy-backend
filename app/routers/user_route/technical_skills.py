import hashlib
import smtplib
from random import randbytes
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter, Request
from ... import utils, oauth2
from app.models import models
from app.schemas.user_schemas import technical_skills_schema
from ...database import get_db, engine
from sqlalchemy.orm import Session
from app.email import Email

router = APIRouter(
    prefix='/users',
    tags=['Users Technical Skills']
)

# ! Get Technical Skills


@router.get('/techskills/{profileId}')
async def get_user_technical_skills(profileId: int, db: Session = Depends(get_db)):

    # query_user = db.query(models.UserProfile).filter(models.UserProfile.profileId ==
    #                                                  current_user.id).first()

    # if not query_user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Data does not exist")

    query_techSkills = db.query(models.TechnicalSkills).filter(
        models.TechnicalSkills.userProfileId == profileId).order_by(models.TechnicalSkills.id).all()

    if not query_techSkills:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Data does not exist")

    return query_techSkills


# ! Create Technical Skills
@router.post('/techskills/', status_code=status.HTTP_201_CREATED)
async def add_technical_skill(body: technical_skills_schema.CreateTechnicalSkill, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):

    query_user = db.query(models.UserProfile).filter(models.UserProfile.profileId ==
                                                     current_user.id).first()

    if not query_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden Request")

    new_skill = models.TechnicalSkills(
        userProfileId=query_user.id, **body.dict())

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill


#! Update Technical Skills
@router.patch('/techskills/{id}', status_code=status.HTTP_200_OK)
async def update_technical_skill(id: int, body: technical_skills_schema.UpdateTechnicalSkill, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    query_userProfile = db.query(models.UserProfile).filter(
        models.UserProfile.profileId == current_user.id)
    userProfile = query_userProfile.first()

    if not userProfile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User profile Does not exist!!!')

    print("Current User Id => " + str(current_user.id))
    print("User Profile Id => " + str(userProfile.id))

    query_skills = db.query(models.TechnicalSkills).filter(
        models.TechnicalSkills.id == id)

    skill = query_skills.first()

    if skill == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'0 skill found with id: {id}')

    print("Skill Profile id => "+str(skill.userProfileId))

    if skill.userProfileId != userProfile.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f'Forbidden Request!!!')

    query_skills.update(body.dict(exclude_unset=True),
                        synchronize_session=False)

    db.commit()
    db.refresh(skill)

    return skill


#! Delete Technical Skills
@router.delete('/techskills/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_technical_skill(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    query_userProfile = db.query(models.UserProfile).filter(
        models.UserProfile.profileId == current_user.id)
    userProfile = query_userProfile.first()

    if not userProfile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User profile Does not exist!!!')

    print("Current User Id => " + str(current_user.id))
    print("User Profile Id => " + str(userProfile.id))

    query_skills = db.query(models.TechnicalSkills).filter(
        models.TechnicalSkills.id == id)

    skill = query_skills.first()

    if skill == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No skill found with id: {id}')

    print("Skill Profile id => "+str(skill.userProfileId))

    if skill.userProfileId != userProfile.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f'Forbidden Request!!!')

    query_skills.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
