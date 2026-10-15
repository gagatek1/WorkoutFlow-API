from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.exercise.schemas import ExercisePart
from app.shared.db import OrmBase


class ExerciseModel(OrmBase):
    __tablename__ = "exercises"
    __table_args__ = (
        Index("ix_exercises_workout_page", "workout_id", "created_at", "id"),
        CheckConstraint("sets >= 1", name="sets_positive"),
        CheckConstraint("reps >= 1", name="reps_positive"),
        CheckConstraint("weight >= 0", name="weight_not_negative"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    workout_id: Mapped[str] = mapped_column(String(36), ForeignKey("workouts.id", ondelete="RESTRICT"))
    owner_id: Mapped[str] = mapped_column(String(128), ForeignKey("user_profiles.user_id", ondelete="RESTRICT"))
    name: Mapped[str] = mapped_column(String(200))
    sets: Mapped[int] = mapped_column(Integer)
    reps: Mapped[int] = mapped_column(Integer)
    weight: Mapped[int] = mapped_column(Integer)
    part: Mapped[ExercisePart] = mapped_column(
        Enum(
            ExercisePart,
            name="part",
            native_enum=False,
            create_constraint=True,
            length=20,
            values_callable=lambda e: [m.value for m in e],
        )
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    @property
    def volume(self) -> int:
        return self.sets * self.reps * self.weight
