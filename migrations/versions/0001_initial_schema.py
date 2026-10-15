from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "user_profiles",
        sa.Column("user_id", sa.String(length=128), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("total_weight", sa.BigInteger(), server_default="0", nullable=False),
        sa.Column("workout_quantity", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("total_weight >= 0", name=op.f("ck_user_profiles_total_weight_not_negative")),
        sa.CheckConstraint("workout_quantity >= 0", name=op.f("ck_user_profiles_workout_quantity_not_negative")),
        sa.PrimaryKeyConstraint("user_id", name=op.f("pk_user_profiles")),
    )
    op.create_table(
        "workouts",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("owner_id", sa.String(length=128), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("total_weight", sa.BigInteger(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("total_weight >= 0", name=op.f("ck_workouts_total_weight_not_negative")),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["user_profiles.user_id"],
            name=op.f("fk_workouts_owner_id_user_profiles"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_workouts")),
    )
    op.create_index("ix_workouts_owner_page", "workouts", ["owner_id", "created_at", "id"], unique=False)
    op.create_table(
        "exercises",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("workout_id", sa.String(length=36), nullable=False),
        sa.Column("owner_id", sa.String(length=128), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("sets", sa.Integer(), nullable=False),
        sa.Column("reps", sa.Integer(), nullable=False),
        sa.Column("weight", sa.Integer(), nullable=False),
        sa.Column(
            "part",
            sa.Enum(
                "back",
                "biceps",
                "chest",
                "core",
                "legs",
                "shoulders",
                "triceps",
                name="part",
                native_enum=False,
                create_constraint=False,
                length=20,
            ),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "part IN ('back', 'biceps', 'chest', 'core', 'legs', 'shoulders', 'triceps')",
            name=op.f("ck_exercises_part"),
        ),
        sa.CheckConstraint("reps >= 1", name=op.f("ck_exercises_reps_positive")),
        sa.CheckConstraint("sets >= 1", name=op.f("ck_exercises_sets_positive")),
        sa.CheckConstraint("weight >= 0", name=op.f("ck_exercises_weight_not_negative")),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["user_profiles.user_id"],
            name=op.f("fk_exercises_owner_id_user_profiles"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["workout_id"], ["workouts.id"], name=op.f("fk_exercises_workout_id_workouts"), ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_exercises")),
    )
    op.create_index("ix_exercises_workout_page", "exercises", ["workout_id", "created_at", "id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_exercises_workout_page", table_name="exercises")
    op.drop_table("exercises")
    op.drop_index("ix_workouts_owner_page", table_name="workouts")
    op.drop_table("workouts")
    op.drop_table("user_profiles")
