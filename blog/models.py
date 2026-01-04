from blog.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="blogs")

    def __str__(self):
        return f"Blog(id={self.id}, title='{self.title}', published={self.published})"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    blogs = relationship("Blog", back_populates="owner")
