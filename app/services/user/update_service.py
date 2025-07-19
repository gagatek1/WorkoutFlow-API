from app.models.user import User
from app.schemas.user import User as UpdateUser


def update_service(update_profile: UpdateUser, db, cognito_user):
    user = (
        db.query(User).filter(User.cognito_id == cognito_user.get("Username")).first()
    )

    if update_profile.first_name is not None:
        user.first_name = update_profile.first_name
    if update_profile.last_name is not None:
        user.last_name = update_profile.last_name

    db.commit()
    db.refresh(user)

    return user
