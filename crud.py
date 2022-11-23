from sqlalchemy.orm import Session
import models
import schemas
from sqlalchemy import update


def get_address(db: Session, id: int):
    return db.query(models.Address).filter(models.Address.id == id).first()


def get_address_by_email(db: Session, email: str):
    return db.query(models.Address).filter(models.Address.email == email).first()


def get_addresses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Address).offset(skip).limit(limit).all()


def create_address(db: Session, address: schemas.Address):
    addr = models.Address(**address.dict())
    db.add(addr)
    db.commit()
    db.refresh(addr)
    return addr


def update_address(db: Session,  id: int, address: schemas.Address):
    stored_addr = db.query(models.Address).filter(models.Address.id == id).first()
    for var, value in vars(address).items():
        setattr(stored_addr, var, value) if value else None
    db.add(stored_addr)
    db.commit()
    db.refresh(stored_addr)
    return stored_addr
