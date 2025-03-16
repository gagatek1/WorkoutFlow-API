from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class UserProfile(Base):
    __tablename__ = "user_profile"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    total_weight = Column(Integer, default=0)
    workout_quantity = Column(Integer, default=0)
    user_id = Column(String, unique=True, nullable=False, index=True)
    workouts = relationship("Workout", back_populates="profile")
