from datetime import datetime
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .. import utils, oauth2
# Models
from app.models import models
from app.models import applications_model
# Schemas
from app.schemas import schemas, applications_schema
from app.schemas import schemas, recruiter_schema
from ..database import get_db, engine
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/recruiter',
    tags=['Recruiter']
)


@router.get('/me')
def get_my_profile(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):

    if current_user.profileType != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Allowed!!!")

    recruiter_query = db.query(models.RecruiterProfile).filter(models.RecruiterProfile.owner_id ==
                                                               current_user.id)

    recruiter = recruiter_query.first()

    # For updating Last Login
    recruiter_query.update({'lastLogin': datetime.now()},
                           synchronize_session=False)

    if not recruiter:
        return JSONResponse(jsonable_encoder({
            'status_code': 404,
            'message': 'Recruiter not created yet',
            'data': []
        }))

    db.commit()
    db.refresh(recruiter)
    db.refresh(current_user)

    return JSONResponse(jsonable_encoder({"userData": current_user, "recruiterData": recruiter}))


@router.get('/{id}', response_model=recruiter_schema.RecruiterResponse)
async def get_profile(id: int, db: Session = Depends(get_db)):

    recruiter_query = db.query(models.RecruiterProfile).filter(
        models.RecruiterProfile.id == id)

    recruiter = recruiter_query.first()

    if not recruiter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Data does not exist")

    return recruiter


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_recruiter(body: recruiter_schema.CreateRecruiter, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):

    query_recruiter = db.query(models.RecruiterProfile).filter(
        models.RecruiterProfile.owner_id == current_user.id).first()

    if query_recruiter:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Recruiter already exist')

    new_recruiter = models.RecruiterProfile(
        owner_id=current_user.id, **body.dict())

    db.add(new_recruiter)
    db.commit()
    db.refresh(new_recruiter)

    return new_recruiter


@router.patch('/me', status_code=status.HTTP_200_OK, response_model=recruiter_schema.RecruiterResponse)
async def update_recruiter(body: recruiter_schema.UpdateRecruiter, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    query_recruiter = db.query(models.RecruiterProfile).filter(
        models.RecruiterProfile.owner_id == current_user.id)
    recruiter = query_recruiter.first()

    if not recruiter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Recruiter Does not exist!!!')

    query_recruiter.update(body.dict(exclude_unset=True),
                           synchronize_session=False)
    db.commit()

    return recruiter


@router.get('/{post_id}/applications', response_model=List[applications_schema.ApplicationUserDetailsRes], summary="Get Applications By Post Id")
async def get_applications(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):

    applications = db.query(applications_model.Applications,
                            models.User
                            ).outerjoin(models.User, models.User.id == applications_model.Applications.userId).filter(
        applications_model.Applications.postId == post_id).all()

    if not applications:
        return JSONResponse(jsonable_encoder({
            'status_code': 404,
            'message': f'Application does not exist with post id: {post_id}',
            'data': []
        }))

    return applications


@router.get('/{recruiterId}/all', response_model=List[applications_schema.ApplicationUserDetailsRes], summary="Get All Applications By Recruiter Id")
async def get_applications_by_recruiter(recruiterId: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):

    applications = db.query(applications_model.Applications,
                            models.User
                            ).outerjoin(models.User, models.User.id == applications_model.Applications.userId).filter(
        applications_model.Applications.recruiterId == recruiterId).all()

    if not applications:
        return JSONResponse(jsonable_encoder({
            'status_code': 404,
            'message': f'Application does not exist with recruiter id: {recruiterId}',
            'data': []
        }))

    result = applications

    return result
