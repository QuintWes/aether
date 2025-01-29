from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Pokemon(Base):
    __tablename__ = "pokemon"

    pokemon_id = Column(Integer, primary_key=True)
    pokemon_name = Column(String, nullable=False)
    form_name = Column(String, nullable=True)
    shiny = Column(Boolean, nullable=False)
    color_1 = Column(String, nullable=True)
    color_2 = Column(String, nullable=True)
    color_3 = Column(String, nullable=True)
    img_url = Column(String, nullable=True)
