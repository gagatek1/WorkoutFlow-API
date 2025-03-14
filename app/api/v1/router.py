from fastapi import APIRouter

from app.api.v1.endpoints.auth_endpoint import auth_router

router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)
