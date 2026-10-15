from concurrent.futures import ThreadPoolExecutor

import pytest

from app.domain.exercise.command_handlers.create_exercise import create_exercise_handler
from app.domain.exercise.command_handlers.delete_exercise import delete_exercise_handler
from app.domain.exercise.commands.create_exercise import CreateExerciseCommand
from app.domain.exercise.commands.delete_exercise import DeleteExerciseCommand
from app.domain.profile.query_service import ProfileQueryService
from app.domain.workout.query_service import WorkoutQueryService
from app.shared.db import get_engine
from tests.fixtures.factories import ExerciseModelFactory, WorkoutModelFactory

pytestmark = pytest.mark.skipif(
    get_engine().dialect.name == "sqlite", reason="SQLite ignores FOR UPDATE; set TEST_DATABASE_URL to a Postgres DB"
)


def _create(workout_id: str) -> None:
    create_exercise_handler(
        CreateExerciseCommand(
            workout_id=workout_id, actor_id="alice", name="Row", sets=1, reps=1, weight=10, part="back"
        )
    )


@pytest.mark.usefixtures("db")
class TestExerciseTotalsUnderConcurrency:
    def test_parallel_writes_on_two_workouts_lose_no_update_and_do_not_deadlock(self) -> None:
        first, second = WorkoutModelFactory.create(), WorkoutModelFactory.create()
        doomed = ExerciseModelFactory.create_batch(5, workout_id=first.id)

        with ThreadPoolExecutor(max_workers=5) as pool:
            jobs = [pool.submit(_create, workout.id) for workout in (first, second) * 10]
            jobs += [
                pool.submit(
                    delete_exercise_handler,
                    DeleteExerciseCommand(workout_id=first.id, exercise_id=exercise.id, actor_id="alice"),
                )
                for exercise in doomed
            ]
            for job in jobs:
                job.result()

        assert WorkoutQueryService().get_workout(first.id, "alice").total_weight == 100
        assert WorkoutQueryService().get_workout(second.id, "alice").total_weight == 100
        assert ProfileQueryService().get_profile("alice").total_weight == 200
