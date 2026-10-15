from app.shared.errors import ConflictError, NotFoundError


class WorkoutNotFoundError(NotFoundError):
    default_message = "Workout not found"


class WorkoutHasExercisesError(ConflictError):
    default_message = "Delete the workout's exercises first"
