from sqlalchemy.orm import Session

import models
import schemas

# CRUD Operations for the DB

# Returns the address for the given id
def get_address(db: Session, id: int):
    return db.query(models.Address).filter(models.Address.id == id).first()


# Returns the address for the given email
def get_address_by_email(db: Session, email: str):
    return db.query(models.Address).filter(models.Address.email == email).first()


# Get the address for the given offset. Enabling paged operations
def get_addresses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Address).offset(skip).limit(limit).all()


# Create address in the DB
def create_address(db: Session, address: schemas.Address):
    addr = models.Address(**address.dict())
    db.add(addr)
    db.commit()
    db.refresh(addr)
    return addr


# Update the address in the DB
def update_address(db: Session, id: int, address: schemas.Address):
    stored_addr = db.query(models.Address).filter(models.Address.id == id).first()
    for var, value in vars(address).items():
        setattr(stored_addr, var, value) if value else None
    db.add(stored_addr)
    db.commit()
    db.refresh(stored_addr)
    return stored_addr
