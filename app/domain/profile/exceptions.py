from app.shared.errors import AlreadyExistsError, NotFoundError


class ProfileNotFoundError(NotFoundError):
    default_message = "Profile not found"


class ProfileAlreadyExistsError(AlreadyExistsError):
    default_message = "Profile already exists"
