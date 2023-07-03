from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import exc

from . import models, schemas

def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()

def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post: return False
    db.delete(db_post)
    db.commit()
    return True

def edit_post(db: Session, post: schemas.Post):
    db_post = db.query(models.Post).filter(models.Post.id == post.id).first()
    db_post.title = post.title
    db_post.content = post.content
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def create_post(db: Session, post: schemas.PostCreate):
    try:
        db_post = models.Post(title=post.title, content=post.content)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except exc.SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error

