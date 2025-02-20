from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    profile_picture = Column(String(255), nullable=True)
    occupation = Column(String(100))
    address = relationship("Address", back_populates="user", uselist=False)


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    address_line_one = Column(String(100))
    address_line_two = Column(String(100), nullable=True)
    city = Column(String(50))
    country = Column(String(50))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="address")

#defineDBasesUsingSQLAlchemyORM
#usrHasoneaddrsStoredInSeprteTble