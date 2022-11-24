import logging
from logging.config import dictConfig

from fastapi import Depends, FastAPI, HTTPException
from geopy.distance import geodesic
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

# Setup Logging
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


# Dependency setup
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Takes the POST data, serializes it to Address model and then saves it in the DB
@app.post("/addresses/", response_model=schemas.Address)
def create_address(address: schemas.Address, db: Session = Depends(get_db)):
    # Pin Code Length Validation
    if len(address.pin) != 6:
        logger.error("Invalid length for pin code")
        return HTTPException(status_code=400, detail="Pin Code should be 6 characters long")
    logger.debug("Created the address")
    return crud.create_address(db=db, address=address)


# Reads all the address. Optionally supports pagination offsets using skip and limit params
@app.get("/addresses/", response_model=list[schemas.Address])
def read_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    addresses = crud.get_addresses(db, skip=skip, limit=limit)
    logger.debug("Reading address from %s with limit %s", str(skip), str(limit))
    return addresses


# Reads the address by taking id
@app.get("/addresses/{id}", response_model=schemas.Address)
def read_address(id: int, db: Session = Depends(get_db)):
    db_addr = crud.get_address(db, id=id)
    if db_addr is None:
        logger.error("Address not found with id: %s", str(id))
        raise HTTPException(status_code=404, detail="Address not found")
    logger.debug("Reading address by id %s", str(id))
    return db_addr


# Reads the address by taking email
@app.get("/addresses/email/{email}", response_model=schemas.Address)
def read_address_by_email(email: str, db: Session = Depends(get_db)):
    db_addr = crud.get_address_by_email(db, email=email)
    if db_addr is None:
        logger.error("Address not found by email: %s", email)
        raise HTTPException(status_code=404, detail="Address not found")
    logger.debug("Reading address by email: %s", email)
    return db_addr


# Deleting an address by id
@app.delete("/addresses/{id}")
def delete_address(id: int, db: Session = Depends(get_db)):
    db_addr = crud.get_address(db, id)
    if db_addr is None:
        logger.error("Address not found with id: %s", str(id))
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_addr)
    db.commit()
    logger.debug("Deleted address by id: %s", str(id))
    return {"ok": True}


# Update the address for the given id
@app.patch("/addresses/{id}", response_model=schemas.Address)
def update_address(id: int, address: schemas.Address, db: Session = Depends(get_db)):
    db_addr = crud.get_address(db, id)
    if db_addr is None:
        logger.error("Address not found with id: %s", str(id))
        raise HTTPException(status_code=404, detail="Address not found")
    updated_data = crud.update_address(db, id, address)
    return updated_data


# For the given distance and lat/long pair it return the address which are equal to or less distance
# We are using Geopy library's Geodisc(https://en.wikipedia.org/wiki/Geodesic) method for
# shortest distance calculation
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
            logger.debug("Found address matching the distance parameter by id: %s", addr.id)
            matched_addresses.append(addr)
    return matched_addresses
