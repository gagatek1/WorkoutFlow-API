from datetime import UTC, datetime

from sqlalchemy import BigInteger, CheckConstraint, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.db import OrmBase


class ProfileModel(OrmBase):
    __tablename__ = "user_profiles"
    __table_args__ = (
        CheckConstraint("total_weight >= 0", name="total_weight_not_negative"),
        CheckConstraint("workout_quantity >= 0", name="workout_quantity_not_negative"),
    )

    user_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    total_weight: Mapped[int] = mapped_column(BigInteger, default=0, server_default="0")
    workout_quantity: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
