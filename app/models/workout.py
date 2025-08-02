from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date = Column(Date, default=date.today())
    total_weight = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    user = relationship("User", back_populates="workouts")
    exercises = relationship("Exercise", back_populates="workout")
