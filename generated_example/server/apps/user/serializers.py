import pydantic


class UsernamePath(pydantic.BaseModel):
    username: str


class LoginQuery(pydantic.BaseModel):
    username: str | None = None
    password: str | None = None
