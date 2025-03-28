from fastapi import APIRouter

from app.api.v1.endpoints.auth_endpoint import auth_router
from app.api.v1.endpoints.exercise_endpoint import exercise_router
from app.api.v1.endpoints.user_endpoint import user_router
from app.api.v1.endpoints.user_profile_endpoint import user_profile_router
from app.api.v1.endpoints.workout_endpoint import workout_router

router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)
router.include_router(user_profile_router)
router.include_router(workout_router)
router.include_router(exercise_router)
router.include_router(user_router)
