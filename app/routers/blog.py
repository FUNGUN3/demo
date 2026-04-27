from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from typing import List
from sqlalchemy.sql import func

router = APIRouter(prefix="/blog", tags=["blog"])

# 3. Активные посты, сортировка по дате DESC
@router.get("/posts", response_model=List[schemas.BlogPost])
def get_active_posts(db: Session = Depends(get_db), search: str = ""):
    query = db.query(models.BlogPost).filter(models.BlogPost.is_active == True)
    if search:
        query = query.filter(
            models.BlogPost.title.contains(search) | models.BlogPost.content.contains(search)
        )
    posts = query.order_by(models.BlogPost.published_at.desc()).all()
    return posts

# 4. Увеличение views_count для поста с id
@router.post("/posts/{post_id}/view")
def increment_post_views(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.BlogPost).filter(models.BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.views_count += 1
    db.commit()
    return {"views": post.views_count}

# 5. Количество постов по theme_preference
@router.get("/posts/theme-stats")
def get_theme_stats(db: Session = Depends(get_db)):
    stats = db.query(
        models.BlogPost.theme_preference,
        func.count(models.BlogPost.id).label("count")
    ).group_by(models.BlogPost.theme_preference).all()
    return {s.theme_preference: s.count for s in stats}

# Создание поста (для начального наполнения)
@router.post("/posts", response_model=schemas.BlogPost)
def create_post(post: schemas.BlogPostCreate, db: Session = Depends(get_db)):
    db_post = models.BlogPost(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post