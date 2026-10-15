import datetime as dt

from sqlalchemy import BigInteger, CheckConstraint, Date, DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.db import OrmBase


class WorkoutModel(OrmBase):
    __tablename__ = "workouts"
    __table_args__ = (
        Index("ix_workouts_owner_page", "owner_id", "created_at", "id"),
        CheckConstraint("total_weight >= 0", name="total_weight_not_negative"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    owner_id: Mapped[str] = mapped_column(String(128), ForeignKey("user_profiles.user_id", ondelete="RESTRICT"))
    name: Mapped[str] = mapped_column(String(200))
    date: Mapped[dt.date] = mapped_column(Date)
    total_weight: Mapped[int] = mapped_column(BigInteger, default=0, server_default="0")
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=lambda: dt.datetime.now(dt.UTC))
