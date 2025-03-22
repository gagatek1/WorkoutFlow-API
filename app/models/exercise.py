from enum import Enum as PyEnum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class ExercisePart(PyEnum):
    back = "back"
    biceps = "biceps"
    chest = "chest"
    core = "core"
    legs = "legs"
    shoulders = "shoulders"
    triceps = "triceps"


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    sets = Column(Integer)
    reps = Column(Integer)
    part = Column(Enum(ExercisePart), nullable=False)
    weight = Column(Integer)
    workout_id = Column(Integer, ForeignKey("workouts.id"), index=True, nullable=False)
    workout = relationship("Workout", back_populates="exercises")
