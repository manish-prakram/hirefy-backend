from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import utils, oauth2
from app.models import models
from app.schemas import schemas
from ..database import get_db, engine
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    user_exist = db.query(models.User).filter(
        models.User.email == user.email).first()

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
    return new_user


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


@router.get('/profile')
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
