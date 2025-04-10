from requests_oauthlib import OAuth2Session

from sode.shared.fp import Either, Empty, Left, Option, Right, Value


class AccessToken1:
    """An access token to be used for authorized requests with an OAuth2 client"""

    value: str
    token_type: str

    def __init__(self, value: str, token_type: str):
        self.value = value
        self.token_type = token_type

    @staticmethod
    def expected(value: str, token_type: str) -> Either[str, "AccessToken1"]:
        if len(token_type.strip()) == 0:
            return Left(f"unknown token_type: {repr(token_type)}")

        match value:
            case str(value) if len(value.strip()) > 0:
                return Right(AccessToken1(value.strip(), token_type.strip()))
            case str(value):
                return Left(f"empty value: {repr(value)}")
            case None:
                return Left(f"missing value: {repr(value)}")
            case _ as value:
                return Left(f"unknown type of value: {repr(value)}")

    @staticmethod
    def maybe(value: str, token_type: str = "Bearer") -> Option["AccessToken1"]:
        match value:
            case None:
                return Empty[AccessToken1]()
            case str(_) if len(value.strip()) == 0:
                return Empty[AccessToken1]()
            case str(v):
                return Value(AccessToken1(v.strip(), token_type.strip()))

    def oauth_session(self) -> OAuth2Session:
        return OAuth2Session(token={"access_token": self.value, "token_type": self.token_type})
