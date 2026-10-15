from app.domain.workout.repository import WorkoutRepository
from app.domain.workout.schemas import WorkoutListResponse, WorkoutResponse, WorkoutSummaryResponse
from app.shared.db import unit_of_work
from app.shared.pagination import decode_cursor, encode_cursor


class WorkoutQueryService:
    def get_workout(self, workout_id: str, actor_id: str) -> WorkoutResponse:
        with unit_of_work() as session:
            return WorkoutResponse.model_validate(WorkoutRepository(session).get_owned(workout_id, actor_id))

    def list_workouts(self, actor_id: str, limit: int, cursor: str | None = None) -> WorkoutListResponse:
        after = decode_cursor(cursor)
        with unit_of_work() as session:
            rows = WorkoutRepository(session).list_page(actor_id, limit + 1, after)
        page = rows[:limit]
        next_cursor = encode_cursor(page[-1].created_at, page[-1].id) if len(rows) > limit else None
        return WorkoutListResponse(
            items=[WorkoutSummaryResponse.model_validate(item) for item in page], next_cursor=next_cursor
        )
