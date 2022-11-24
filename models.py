from sqlalchemy import Column, Integer, String, Float

from database import Base


# Main model for holding the address details
class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True, )
    first_name = Column(String)
    last_name = Column(String)
    line1 = Column(String)
    line2 = Column(String)
    city = Column(String)
    state = Column(String)
    pin = Column(String)
    lat = Column(Float)
    long = Column(Float)
    email = Column(String, index=True)
    label = Column(String)
