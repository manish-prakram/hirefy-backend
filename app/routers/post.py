from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from ..schemas import posts_schema
from ..models import models
from fastapi.encoders import jsonable_encoder

from ..database import get_db, engine
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import oauth2

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


# ! Get All Posts Without Login
@router.get('/', response_model=List[posts_schema.PostOut])
def get_all_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    result = db.query(models.Post, func.count(models.Review.post_id).label("reviews")).join(
        models.Review, models.Review.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() ## For same user posts only

    return result


# ! Get my all posts
@router.get('/my', status_code=status.HTTP_200_OK)
async def get_my_all_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post, func.count(models.Review.post_id).label("reviews")).join(
        models.Review, models.Review.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id).all()

    # if not post:
    #     return JSONResponse(content=f'No post found with id: {current_user.id}')

    return post


#! Get one Post without Login
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=posts_schema.PostOut)
async def get_one_post(id: int, db: Session = Depends(get_db), ):

    post = db.query(models.Post, func.count(models.Review.post_id).label("reviews")).join(
        models.Review, models.Review.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        return JSONResponse(jsonable_encoder({
            'status_code': 404,
            'message': f'Post does not exist with id: {id}',
            'data': []
        }))

    return post


#! Create New Post
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=posts_schema.PostResponse)
def create_post(post_body: posts_schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    query_recruiter = db.query(models.RecruiterProfile).filter(
        models.RecruiterProfile.owner_id == current_user.id).first()

    new_post = models.Post(owner_id=current_user.id,
                           recruiterId=query_recruiter.id, **post_body.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


#! Update my post
@router.patch('/{id}', response_model=posts_schema.PostResponse)
async def update_post(id: int, update_post: posts_schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'0 posts found with id: {id}')

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f'Forbidden Request!!!')

    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


# ! Delete my post
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No data found with id: {id}")

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Forbidden Request!")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
