from fastapi import APIRouter, Request

from app.domain.profile.query_service import ProfileQueryService
from app.domain.profile.schemas import ProfileResponse
from app.shared.auth.authorize import authorize_user

router = APIRouter(tags=["profiles"])

PROFILE_QUERY_SERVICE = ProfileQueryService()


@router.get("/profiles/me", description="Get the caller's profile (names and workout totals).")
def show_profile(request: Request) -> ProfileResponse:
    with authorize_user(request.headers) as user:
        return PROFILE_QUERY_SERVICE.get_profile(user.id)
