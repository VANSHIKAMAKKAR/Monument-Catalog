from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Places(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User , cascade="save-update")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class PopularLocations(Base):
    __tablename__ = 'popular_locations'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(2500))
    year = Column(Integer)
    founder = Column(String(250))
    places_id = Column(Integer, ForeignKey('places.id'))
    places = relationship(Places , cascade="save-update")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User , cascade="save-update")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
        }


engine = create_engine('sqlite:///itemcatalogappwithlogin.db')


Base.metadata.create_all(engine)
