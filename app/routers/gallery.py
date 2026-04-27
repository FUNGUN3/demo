from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from typing import List

router = APIRouter(prefix="/gallery", tags=["gallery"])

# 3. Все изображения категории (по умолчанию все, сортировка по views)
@router.get("/images", response_model=List[schemas.GalleryImage])
def get_images(category: str = None, db: Session = Depends(get_db)):
    query = db.query(models.GalleryImage)
    if category:
        query = query.filter(models.GalleryImage.category == category)
    return query.order_by(models.GalleryImage.views.desc()).all()

# 4. Увеличить views для изображения
@router.post("/images/{image_id}/view")
def increment_image_views(image_id: int, db: Session = Depends(get_db)):
    image = db.query(models.GalleryImage).filter(models.GalleryImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    image.views += 1
    db.commit()
    return {"views": image.views}

# 5. Топ-3 самых просматриваемых
@router.get("/images/top", response_model=List[schemas.GalleryImage])
def get_top_images(db: Session = Depends(get_db)):
    return db.query(models.GalleryImage).order_by(models.GalleryImage.views.desc()).limit(3).all()

# Создание изображения (для наполнения)
@router.post("/images", response_model=schemas.GalleryImage)
def create_image(image: schemas.GalleryImageCreate, db: Session = Depends(get_db)):
    db_image = models.GalleryImage(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image