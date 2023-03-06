
from datetime import datetime
from random import randbytes
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter, Request
from .. import utils, oauth2
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Models
from app.models import models
from app.models import applications_model
# Schemas
from app.schemas import schemas, applications_schema
from ..database import get_db, engine
from sqlalchemy.orm import Session
from app.email import Email

router = APIRouter(
    prefix='/application',
    tags=['Candidate Applications']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_application(application: applications_schema.CreateApplication, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(
        models.Post.id == application.postId).first()
    if not post:
        return {"message": f"Post with id:{application.postId} does not exist"}

    if current_user.profileType != 1:
        return {"message": "only candidates profile are allowed"}

    application_query = db.query(applications_model.Applications).filter(
        applications_model.Applications.postId == application.postId,
        applications_model.Applications.userId == current_user.id,
    )

    found_application = application_query.first()

    if found_application:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"user {current_user.id} has already applied on {application.postId}")

    if (application.status == 1):
        new_application = applications_model.Applications(
            userId=current_user.id,
            postId=application.postId,
            status=application.status,
            owner_id=post.owner_id,
            recruiterId=post.recruiterId,
        )

        db.add(new_application)
        db.commit()
        db.refresh(new_application)

        return {"message": "successfully applied on application", "data": new_application}

    else:
        # return {"message": "only status 1 is allowed"}

        if found_application == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Application does not exist")


@router.get('/', response_model=List[applications_schema.ApplicationUserDetailsRes], summary='All Applications with users details')
async def get_applications(db: Session = Depends(get_db)):

    applications = db.query(applications_model.Applications,
                            models.User
                            ).outerjoin(models.User, models.User.id == applications_model.Applications.userId).all()
    
    if not applications:
        return JSONResponse(jsonable_encoder({
            'status_code': 404,
            'message': f'Application does not exist',
            'data': []
        }))

    return applications


@router.patch('/update')
async def update_application_status(data: applications_schema.UpdateApplicationStatus, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    application_query = db.query(applications_model.Applications).filter(
        applications_model.Applications.id == data.id)

    application_found = application_query.first()

    if not application_found:
        return JSONResponse(jsonable_encoder({
            'status_code': 404,
            'message': f'Application does not exist with id: {data.id}',
            'data': []
        }))

    application_query.update(
        {
            'status': data.status,
            'updatedAt': datetime.now(),
        })

    db.commit()
    db.refresh(application_found)

    return JSONResponse(jsonable_encoder({
        'status_code': status.HTTP_200_OK,
        'message': f'Successfully updated',
        'data': application_found
    }))
