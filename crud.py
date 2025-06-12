from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User, Purchase, Earning
from utils import generate_referral_code

def register_user(name: str, email: str, referred_by_code: str | None, db: Session):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    referral_code = generate_referral_code()
    new_user = User(name=name, email=email, referral_code=referral_code)

    if referred_by_code:
        referrer = db.query(User).filter(User.referral_code == referred_by_code).first()
        if not referrer:
            raise HTTPException(status_code=400, detail="Invalid referral code")
        if db.query(User).filter(User.referred_by == referrer.id).count() >= 8:
            raise HTTPException(status_code=400, detail="Referrer has reached limit of 8 referrals")
        new_user.referred_by = referrer.id
        new_user.level = referrer.level + 1

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered", "referral_code": new_user.referral_code}


def make_purchase(user_id: int, amount: float, db: Session):
    if amount < 1000:
        return {"msg": "No earnings recorded as purchase is below threshold"}

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    purchase = Purchase(user_id=user.id, amount=amount)
    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    earnings = []
    if user.referred_by:
        ref_lvl_1 = db.query(User).filter(User.id == user.referred_by).first()
        if ref_lvl_1:
            earnings.append(Earning(user_id=ref_lvl_1.id, source_user_id=user.id, purchase_id=purchase.id, amount=round(0.05 * amount, 2), level=1))
            if ref_lvl_1.referred_by:
                ref_lvl_2 = db.query(User).filter(User.id == ref_lvl_1.referred_by).first()
                if ref_lvl_2:
                    earnings.append(Earning(user_id=ref_lvl_2.id, source_user_id=user.id, purchase_id=purchase.id, amount=round(0.01 * amount, 2), level=2))

    db.bulk_save_objects(earnings)
    db.commit()
    return {"msg": "Purchase recorded and earnings distributed"}

def get_earnings(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    earnings = db.query(Earning).filter(Earning.user_id == user_id).all()
    total = sum([float(e.amount) for e in earnings])
    breakdown = {"level_1": 0, "level_2": 0}
    for e in earnings:
        if e.level == 1:
            breakdown["level_1"] += float(e.amount)
        elif e.level == 2:
            breakdown["level_2"] += float(e.amount)

    return {"total_earnings": total, "breakdown": breakdown, "transactions": earnings}
