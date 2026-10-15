from app.domain.identity.commands.sign_in import SignInCommand
from app.domain.identity.exceptions import (
    AccountNotConfirmedError,
    AuthChallengeRequiredError,
    InvalidCredentialsError,
    translate,
)
from app.domain.identity.schemas import TokenResponse
from app.shared.clients.cognito import CognitoError, get_cognito

ERRORS = {
    "UserNotFoundException": InvalidCredentialsError,
    "NotAuthorizedException": InvalidCredentialsError,
    "UserNotConfirmedException": AccountNotConfirmedError,
}


def sign_in_handler(command: SignInCommand) -> TokenResponse:
    try:
        result = get_cognito().initiate_auth(
            "USER_PASSWORD_AUTH", command.email, {"USERNAME": command.email, "PASSWORD": command.password}
        )
    except CognitoError as exc:
        raise translate(exc, ERRORS) from exc
    if "AccessToken" not in result:
        raise AuthChallengeRequiredError
    return TokenResponse(
        access_token=result["AccessToken"], refresh_token=result["RefreshToken"], expires_in=result["ExpiresIn"]
    )
