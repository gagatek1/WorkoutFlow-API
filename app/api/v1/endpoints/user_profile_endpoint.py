from fastapi import APIRouter, Depends

from app.core.database import db_dependency
from app.core.security import get_token
from app.schemas.user_profile import UserProfile
from app.services.user_profile.get_service import get_service
from app.services.user_profile.update_service import update_service

user_profile_router = APIRouter(prefix="/profiles", tags=["profiles"])


@user_profile_router.put("/update/{profile_id}")
async def update_profile(
    profile_id,
    update_profile: UserProfile,
    db: db_dependency,
    user: dict = Depends(get_token),
):
    return update_service(profile_id, update_profile, db, user)


@user_profile_router.get("/{profile_id}")
async def get_profile(profile_id, db: db_dependency, user: dict = Depends(get_token)):
    return get_service(profile_id, db)
