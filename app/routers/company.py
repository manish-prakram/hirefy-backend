from datetime import datetime
from fastapi import Response, status, APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ..database import get_db
from app.models import models
from app.schemas import company_schema
from .. import oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/company',
    tags=['Company']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_company(body: company_schema.CreateCompany, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    recruiter_query = db.query(models.RecruiterProfile).filter(
        models.RecruiterProfile.owner_id == current_user.id).first()

    # TODO: Company already exist exception

    new_company = models.Company(
        adminId=current_user.id,
        recruiterId=recruiter_query.id,
        **body.dict()
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company


@router.get('/me', status_code=status.HTTP_200_OK)
async def get_my_company(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    if current_user.profileType != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Allowed!!!")

    company_query = db.query(models.Company).filter(
        models.Company.adminId == current_user.id)

    company = company_query.first()

    # Recruiters
    # recruiter_query = db.query(models.RecruiterProfile).filter(models.RecruiterProfile.owner_id ==
    #                                                            current_user.id).all()

    # For updating Last Login
    company_query.update({'lastLogin': datetime.now()},
                         synchronize_session=False)

    if not company:
        return JSONResponse(jsonable_encoder({
            'status_code': 404,
            'message': 'Recruiter not created yet',
            'data': []
        }))

    db.commit()
    db.refresh(current_user)
    db.refresh(company)
    # db.refresh(recruiter_query)

    return JSONResponse(jsonable_encoder({"userData": current_user, "companyData": company}))
