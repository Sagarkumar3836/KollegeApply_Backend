from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    referral_code = Column(String(20), unique=True, index=True)
    referred_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    level = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())
    referrals = relationship("User", remote_side=[id])

class Purchase(Base):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(DECIMAL(10, 2))
    created_at = Column(DateTime, server_default=func.now())

class Earning(Base):
    __tablename__ = 'earnings'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    source_user_id = Column(Integer, ForeignKey('users.id'))
    purchase_id = Column(Integer, ForeignKey('purchases.id'))
    amount = Column(DECIMAL(10, 2))
    level = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
