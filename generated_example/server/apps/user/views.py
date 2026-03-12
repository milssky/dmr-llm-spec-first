from datetime import UTC, datetime, timedelta
from http import HTTPStatus

from django.http import HttpResponse

from dmr import (
    Blueprint,
    Body,
    HeaderSpec,
    Path,
    Query,
    ResponseSpec,
    modify,
    validate,
)
from dmr.errors import ErrorModel
from dmr.parsers import FormUrlEncodedParser
from dmr.plugins.msgspec import MsgspecJsonParser, MsgspecJsonRenderer
from dmr.plugins.pydantic import PydanticSerializer

from server.apps.common.media_types import XmlStrictStubParser, XmlStrictStubRenderer
from server.apps.common.serializers import User
from server.apps.user.serializers import LoginQuery, UsernamePath

_NO_BODY_CONTENT_TYPE = {"application/x.no-body"}


class CreateUserBlueprint(
    Body[User],
    Blueprint[PydanticSerializer],
):
    parsers = (
        MsgspecJsonParser(),
        XmlStrictStubParser(),
        FormUrlEncodedParser(),
    )
    renderers = (MsgspecJsonRenderer(), XmlStrictStubRenderer())
    responses = (
        ResponseSpec(
            ErrorModel,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        ),
    )

    @modify(
        status_code=HTTPStatus.OK,
        operation_id="createUser",
        tags=["user"],
        summary="Create user.",
        description="This can only be done by the logged in user.",
    )
    def post(self) -> User:
        # TODO: persist created user.
        return self.parsed_body


class CreateUsersWithListInputBlueprint(
    Body[list[User]],
    Blueprint[PydanticSerializer],
):
    parsers = (MsgspecJsonParser(),)
    renderers = (MsgspecJsonRenderer(), XmlStrictStubRenderer())
    responses = (
        ResponseSpec(
            ErrorModel,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        ),
    )

    @modify(
        status_code=HTTPStatus.OK,
        operation_id="createUsersWithListInput",
        tags=["user"],
        summary="Creates list of users with given input array.",
        description="Creates list of users with given input array.",
    )
    def post(self) -> User:
        users = self.parsed_body
        if users:
            return users[0]
        return User(username="placeholder-user")


class LoginUserBlueprint(
    Query[LoginQuery],
    Blueprint[PydanticSerializer],
):
    renderers = (MsgspecJsonRenderer(), XmlStrictStubRenderer())

    @validate(
        ResponseSpec(
            str,
            status_code=HTTPStatus.OK,
            headers={
                "X-Rate-Limit": HeaderSpec(
                    description="calls per hour allowed by the user",
                    required=False,
                ),
                "X-Expires-After": HeaderSpec(
                    description="date in UTC when token expires",
                    required=False,
                ),
            },
        ),
        ResponseSpec(
            ErrorModel,
            status_code=HTTPStatus.BAD_REQUEST,
        ),
        ResponseSpec(
            ErrorModel,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        ),
        operation_id="loginUser",
        tags=["user"],
        summary="Logs user into the system.",
        description="log user into the system.",
    )
    def get(self) -> HttpResponse:
        expires = datetime.now(UTC) + timedelta(hours=1)
        return self.to_response(
            f"logged in user session for {self.parsed_query.username or 'guest'}",
            status_code=HTTPStatus.OK,
            headers={
                "X-Rate-Limit": "1000",
                "X-Expires-After": expires.isoformat(),
            },
        )


class LogoutUserBlueprint(Blueprint[PydanticSerializer]):
    @validate(
        ResponseSpec(
            None,
            status_code=HTTPStatus.OK,
            limit_to_content_types=_NO_BODY_CONTENT_TYPE,
        ),
        validate_responses=False,
        operation_id="logoutUser",
        tags=["user"],
        summary="Logs out current logged in user session.",
        description="Log user out of system.",
    )
    def get(self) -> HttpResponse:
        return HttpResponse(status=HTTPStatus.OK)


class GetUserByNameBlueprint(
    Path[UsernamePath],
    Blueprint[PydanticSerializer],
):
    renderers = (MsgspecJsonRenderer(), XmlStrictStubRenderer())
    responses = (
        ResponseSpec(ErrorModel, status_code=HTTPStatus.BAD_REQUEST),
        ResponseSpec(ErrorModel, status_code=HTTPStatus.NOT_FOUND),
        ResponseSpec(
            ErrorModel,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        ),
    )

    @modify(
        operation_id="getUserByName",
        tags=["user"],
        summary="Get user by user name.",
        description="Get user details based on username.",
    )
    def get(self) -> User:
        return User(username=self.parsed_path.username)


class UpdateUserBlueprint(
    Path[UsernamePath],
    Body[User],
    Blueprint[PydanticSerializer],
):
    parsers = (
        MsgspecJsonParser(),
        XmlStrictStubParser(),
        FormUrlEncodedParser(),
    )
    @validate(
        ResponseSpec(
            None,
            status_code=HTTPStatus.OK,
            limit_to_content_types=_NO_BODY_CONTENT_TYPE,
        ),
        ResponseSpec(
            ErrorModel,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        ),
        validate_responses=False,
        operation_id="updateUser",
        tags=["user"],
        summary="Update user.",
        description="This can only be done by the logged in user.",
    )
    def put(self) -> HttpResponse:
        # TODO: persist updated user.
        return HttpResponse(status=HTTPStatus.OK)


class DeleteUserBlueprint(
    Path[UsernamePath],
    Blueprint[PydanticSerializer],
):
    @validate(
        ResponseSpec(
            None,
            status_code=HTTPStatus.OK,
            limit_to_content_types=_NO_BODY_CONTENT_TYPE,
        ),
        ResponseSpec(ErrorModel, status_code=HTTPStatus.BAD_REQUEST),
        ResponseSpec(ErrorModel, status_code=HTTPStatus.NOT_FOUND),
        ResponseSpec(
            ErrorModel,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        ),
        validate_responses=False,
        operation_id="deleteUser",
        tags=["user"],
        summary="Delete user.",
        description="This can only be done by the logged in user.",
    )
    def delete(self) -> HttpResponse:
        # TODO: implement user deletion.
        return HttpResponse(status=HTTPStatus.OK)
