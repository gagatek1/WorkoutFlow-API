from app.domain.exercise.repository import ExerciseRepository
from app.domain.exercise.schemas import ExerciseListResponse, ExerciseResponse, ExerciseSummaryResponse
from app.domain.workout.repository import WorkoutRepository
from app.shared.db import unit_of_work
from app.shared.pagination import decode_cursor, encode_cursor


class ExerciseQueryService:
    def get_exercise(self, workout_id: str, exercise_id: str, actor_id: str) -> ExerciseResponse:
        with unit_of_work() as session:
            exercise = ExerciseRepository(session).get_owned(workout_id, exercise_id, actor_id)
            return ExerciseResponse.model_validate(exercise)

    def list_exercises(
        self, workout_id: str, actor_id: str, limit: int, cursor: str | None = None
    ) -> ExerciseListResponse:
        after = decode_cursor(cursor)
        with unit_of_work() as session:
            WorkoutRepository(session).get_owned(workout_id, actor_id)
            rows = ExerciseRepository(session).list_page(workout_id, limit + 1, after)
        page = rows[:limit]
        next_cursor = encode_cursor(page[-1].created_at, page[-1].id) if len(rows) > limit else None
        return ExerciseListResponse(
            items=[ExerciseSummaryResponse.model_validate(item) for item in page], next_cursor=next_cursor
        )
