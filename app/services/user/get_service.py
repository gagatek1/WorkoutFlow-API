from fastapi import HTTPException

from app.models.user import User


def get_service(user_id, db):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="Not found")

    return user


def me_service(db, cognito_user):
    user = (
        db.query(User).filter(User.cognito_id == cognito_user.get("Username")).first()
    )

    return user
