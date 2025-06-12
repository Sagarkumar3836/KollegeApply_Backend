from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register_user(name: str, email: str, referred_by_code: str | None = None, db: Session = Depends(get_db)):
    return crud.register_user(name, email, referred_by_code, db)

@router.post("/purchase")
def purchase(user_id: int, amount: float, db: Session = Depends(get_db)):
    return crud.make_purchase(user_id, amount, db)

@router.get("/earnings/{user_id}")
def earnings(user_id: int, db: Session = Depends(get_db)):
    return crud.get_earnings(user_id, db)
