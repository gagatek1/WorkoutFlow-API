from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    total_weight = Column(Integer, default=0)
    workout_id = Column(Integer, ForeignKey("workouts.id"), index=True, nullable=False)
    workout = relationship("Workout", back_populates="exercises")
