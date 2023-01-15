from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import utils, oauth2
from app.models import models
from app.schemas import schemas, recruiter_schema
from ..database import get_db, engine
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/recruiter',
    tags=['Recruiter']
)


@router.get('/')
def get_profile(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):

    if current_user.profileType != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Allowed!!!")

    recruiter = db.query(models.RecruiterProfile).filter(models.RecruiterProfile.owner_id ==
                                                         current_user.id).first()  # For same user posts only

    if not recruiter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Data does not exist")
    print(recruiter)
    return {"userData": current_user, "recruiterData": recruiter}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_recruiter(body: recruiter_schema.CreateRecruiter, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):

    new_recruiter = models.RecruiterProfile(
        owner_id=current_user.id, **body.dict())

    db.add(new_recruiter)
    db.commit()
    db.refresh(new_recruiter)

    return new_recruiter
