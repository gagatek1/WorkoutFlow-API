from app.shared.errors import NotFoundError


class ExerciseNotFoundError(NotFoundError):
    default_message = "Exercise not found"
