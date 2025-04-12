from requests_oauthlib import OAuth2Session

from sode.shared.fp import Either, Empty, Left, Option, Right, Value


class AccessToken:
    """An access token to be used for authorized requests with an OAuth2 client"""

    value: str
    token_type: str

    def __init__(self, value: str, token_type: str):
        self.value = value
        self.token_type = token_type

    @staticmethod
    def expected(value: str, token_type: str) -> Either[str, "AccessToken"]:
        if (token_type is None) or (len(token_type.strip()) == 0):
            return Left(f"unknown token_type: {token_type!r}")

        match value:
            case str(value) if len(value.strip()) > 0:
                return Right(AccessToken(value.strip(), token_type.strip()))
            case str(value):
                return Left(f"empty value: {value!r}")
            case None:
                return Left(f"missing value: {value!r}")
            case _ as value:
                return Left(f"unknown type of value: {value!r}")

    @staticmethod
    def maybe(value: str, token_type: str) -> Option["AccessToken"]:
        match AccessToken.expected(value, token_type):
            case Left(_):
                return Empty()
            case Right(t):
                return Value(t)

    def oauth_session(self) -> OAuth2Session:
        return OAuth2Session(token={"access_token": self.value, "token_type": self.token_type})
