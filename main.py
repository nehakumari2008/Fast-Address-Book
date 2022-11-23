from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from geopy.distance import geodesic

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/addresses/", response_model=schemas.Address)
def create_address(address: schemas.Address, db: Session = Depends(get_db)):
    # Pin Code Length Validation
    if len(address.pin) != 6:
        return HTTPException(status_code=400, detail="Pin Code should be 6 characters long")
    return crud.create_address(db=db, address=address)


@app.get("/addresses/", response_model=list[schemas.Address])
def read_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    addresses = crud.get_addresses(db, skip=skip, limit=limit)
    return addresses


@app.get("/addresses/{id}", response_model=schemas.Address)
def read_address(id: int, db: Session = Depends(get_db)):
    db_addr = crud.get_address(db, id=id)
    if db_addr is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_addr


@app.get("/addresses/email/{email}", response_model=schemas.Address)
def read_address_by_email(email: str, db: Session = Depends(get_db)):
    db_addr = crud.get_address_by_email(db, email=email)
    if db_addr is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_addr


@app.delete("/addresses/{id}")
def delete_address(id: int, db: Session = Depends(get_db)):
    db_addr = crud.get_address(db, id)
    if db_addr is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_addr)
    db.commit()
    return {"ok": True}


@app.patch("/addresses/{id}", response_model=schemas.Address)
def update_address(id: int, address: schemas.Address, db: Session = Depends(get_db)):
    db_addr = crud.get_address(db, id)
    if db_addr is None:
        raise HTTPException(status_code=404, detail="Address not found")
    updated_data = crud.update_address(db, id, address)
    return updated_data


@app.get("/addresses/{distance}/{lat}/{long}")
def get_addr_by_distance(distance: float, lat: float, long: float, db: Session = Depends(get_db)):
    source_coordinates = (lat, long)
    source_distance = distance
    addresses = crud.get_addresses(db)
    matched_addresses = []
    for addr in addresses:
        dest_coordinates = (addr.lat, addr.long)
        distance = geodesic(source_coordinates, dest_coordinates).km
        if distance <= source_distance:
            matched_addresses.append(addr)
    return matched_addresses


