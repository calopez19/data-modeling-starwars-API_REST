from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    create_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    fav_people_user_id: Mapped[list["Favorite_people"]] = relationship(
        back_populates="fav_people_user_id")
    fav_planet_user_id: Mapped[list["Favorite_planets"]] = relationship(
        back_populates="fav_planet_user_id")
    def serialize(self):
        return {
            "id": self.id,
            "username": self.name,
            "email": self.address,
            "create_date": self.create_date,
            "is_active": self.is_active,
        }


class Favorite_people(db.Model):
    __tablename__ = "favorite_people"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True)
    people_id: Mapped[int] = mapped_column(
        ForeignKey("people.id"), primary_key=True)
    added_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    fav_people_user_id: Mapped["User"] = relationship(
        back_populates="fav_people_user_id")
    fav_people_id: Mapped["User"] = relationship(
        back_populates="fav_people_id")
    def serialize(self):
        return {
            "user_id": self.id,
            "people_id": self.people_id,
            "added_date": self.added_date,
        }


class Favorite_planets(db.Model):
    __tablename__ = "favorite_planets"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planet.id"), primary_key=True)
    added_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    fav_planet_user_id: Mapped["User"] = relationship(
        back_populates="fav_planet_user_id")
    fav_planet_id: Mapped["User"] = relationship(
        back_populates="fav_people_id")
    def serialize(self):
        return {
            "user_id": self.id,
            "people_id": self.people_id,
            "added_date": self.added_date,
        }


class People(db.Model):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    height: Mapped[int] = mapped_column(Integer)
    mass: Mapped[int] = mapped_column(Integer)
    hair_color: Mapped[str] = mapped_column(String(30))
    skin_color: Mapped[str] = mapped_column(String(30))
    eye_color: Mapped[str] = mapped_column(String(30))
    birth_year: Mapped[datetime] = mapped_column(DateTime())
    gender: Mapped[str] = mapped_column(String(30))
    fav_people_id: Mapped[list["Favorite_people"]
                          ] = relationship(back_populates="fav_people_id")
    def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
                "height": self.height,
                "mass": self.mass,
                "hair_color": self.hair_color,
                "skin_color": self.skin_color,
                "eye_color": self.eye_color,
                "birth_year": self.birth_year,
                "gender": self.gender,
            }

class Planets(db.Model):
    __tablename__ = "planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    rotation_period: Mapped[int] = mapped_column(Integer)
    orbital_period: Mapped[int] = mapped_column(Integer)
    diameter: Mapped[int] = mapped_column(Integer)
    climate: Mapped[str] = mapped_column(String(120))
    gavity: Mapped[int] = mapped_column(Integer)
    terrain: Mapped[str] = mapped_column(String(120))
    surface_water: Mapped[int] = mapped_column(Integer)
    population: Mapped[int] = mapped_column(Integer)
    fav_planet_id: Mapped[list["Favorite_planets"]
                          ] = relationship(back_populates="fav_planet_id")
    def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
                "rotation_period": self.rotation_period,
                "orbital_period": self.orbital_period,
                "diameter": self.diameter,
                "climate": self.climate,
                "gavity": self.gavity,
                "terrain": self.terrain,
                "surface_water": self.surface_water,
                "population": self.population,
            }