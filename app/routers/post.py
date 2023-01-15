from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..schemas import schemas
from ..models import models

from ..database import get_db, engine
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import oauth2

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    result = db.query(models.Post, func.count(models.Review.post_id).label("reviews")).join(
        models.Review, models.Review.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() ## For same user posts only

    return result


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post_body: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **post_body.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
