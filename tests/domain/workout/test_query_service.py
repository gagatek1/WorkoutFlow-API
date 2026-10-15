import pytest

from app.domain.workout.exceptions import WorkoutNotFoundError
from app.domain.workout.query_service import WorkoutQueryService
from app.domain.workout.schemas import WorkoutResponse
from app.shared.pagination import InvalidCursorError
from tests.fixtures.factories import WorkoutModelFactory


@pytest.mark.usefixtures("db")
class TestWorkoutQueryService:
    def test_get_returns_workout_to_owner(self) -> None:
        workout = WorkoutModelFactory.create()

        assert WorkoutQueryService().get_workout(workout.id, "alice") == WorkoutResponse.model_validate(workout)

    def test_get_by_other_user_is_not_found(self) -> None:
        workout = WorkoutModelFactory.create()

        with pytest.raises(WorkoutNotFoundError):
            WorkoutQueryService().get_workout(workout.id, "mallory")

    def test_list_returns_only_own_workouts_paginated(self) -> None:
        mine = {w.id for w in WorkoutModelFactory.create_batch(3)}
        WorkoutModelFactory.create(owner_id="bob")

        first = WorkoutQueryService().list_workouts("alice", limit=2)
        second = WorkoutQueryService().list_workouts("alice", limit=2, cursor=first.next_cursor)

        assert len(first.items) == 2
        assert second.next_cursor is None
        assert {w.id for w in first.items + second.items} == mine

    def test_list_rejects_tampered_cursor(self) -> None:
        with pytest.raises(InvalidCursorError):
            WorkoutQueryService().list_workouts("alice", limit=2, cursor="garbage")
