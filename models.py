from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__='blogs'
    id= Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="blogs")
    
    
class User(Base):
    __tablename__='users'
    id= Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    description= Column(String)
    password= Column(String)    #password will not be encrypted
    blogs = relationship("Blog", back_populates="creator")
    