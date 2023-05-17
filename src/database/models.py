import enum

from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, func, Boolean, Text, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


tag_to_image = Table('tag_to_image', Base.metadata,
                     #Column('id', Integer, primary_key=True),
                     Column('tag_id', Integer, ForeignKey('tags.id', ondelete="CASCADE"), nullable=False),
                     Column('image_id', Integer, ForeignKey('images.id', ondelete="CASCADE"), nullable=False),
                     )


class UserRole(int, enum.Enum):
    Admin = 1
    Moderator = 2
    User = 3


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String(50), unique=True)
    email = Column(String(150), unique=True)
    role = Column(Integer, default=UserRole.User.value)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())
    user_pic_url = Column(String(255))
    name = Column(String(150), unique=False)
    is_active = Column(Boolean, default=True)
    password_checksum = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    image_url = Column(String(255), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())
    description = Column(String(255))
    is_deleted = Column(Boolean, default=False)
    user = relationship('User', backref="images")
    tags = relationship("Tag", secondary=tag_to_image, backref="images", passive_deletes=True)


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))
    image_id = Column(Integer, ForeignKey(Image.id, ondelete="CASCADE"))
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime)
    comment_text = Column(Text)
    user = relationship('User', backref="comments")
    image = relationship('Image', backref="comments")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag_name = Column(String(25), unique=True)


class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True)
    rate = Column("rate", Integer, default=0)
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))
    image_id = Column(Integer, ForeignKey(Image.id, ondelete="CASCADE"))
    user = relationship('User', backref="ratings")
    image = relationship('Image', backref="ratings")


class BlacklistToken(Base):
    __tablename__ = 'blacklisted_tokens'
    id = Column(Integer, primary_key=True)
    token = Column(String(255), unique=True, nullable=False)
    added_on = Column(DateTime, default=func.now())
