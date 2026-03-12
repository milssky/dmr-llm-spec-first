from http import HTTPStatus

from django.http import HttpResponse

from dmr import (
    Blueprint,
    Body,
    Headers,
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

from server.apps.common.media_types import (
    OctetStreamStrictStubParser,
    XmlStrictStubParser,
    XmlStrictStubRenderer,
)
from server.apps.common.security import ApiKeyHeaderSyncAuth, PetstoreOAuthSyncAuth
from server.apps.common.serializers import ApiResponse, Pet
from server.apps.pet.serializers import (
    DeletePetHeaders,
    FindPetsByStatusQuery,
    FindPetsByTagsQuery,
    PetIdPath,
    UpdatePetWithFormQuery,
    UploadFileQuery,
)

_PET_AUTH = (PetstoreOAuthSyncAuth(("write:pets", "read:pets")),)
_PET_AUTH_OR_API_KEY = (
    ApiKeyHeaderSyncAuth(),
    PetstoreOAuthSyncAuth(("write:pets", "read:pets")),
)
_NO_BODY_CONTENT_TYPE = {"application/x.no-body"}


class UpdatePetBlueprint(
    Body[Pet],
    Blueprint[PydanticSerializer],
):
    auth = _PET_AUTH
    parsers = (
        MsgspecJsonParser(),
        XmlStrictStubParser(),
        FormUrlEncodedParser(),
    )
    renderers = (MsgspecJsonRenderer(), XmlStrictStubRenderer())
    responses = (
        ResponseSpec(ErrorModel, status_code=HTTPStatus.BAD_REQUEST),
        ResponseSpec(ErrorModel, status_code=HTTPStatus.NOT_FOUND),
        ResponseSpec(
            ErrorModel,
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        ResponseSpec(
            ErrorModel,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        ),
    )

    @modify(
        operation_id="updatePet",
        tags=["pet"],
        summary="Update an existing pet.",
        description="Update an existing pet by Id.",
    )
    def put(self) -> Pet:
        # TODO: replace echo behavior with persistence-backed update logic.
        return self.parsed_body


class AddPetBlueprint(
    Body[Pet],
    Blueprint[PydanticSerializer],
):
    auth = _PET_AUTH
    parsers = (
        MsgspecJsonParser(),
        XmlStrictStubParser(),
        FormUrlEncodedParser(),
    )
    renderers = (MsgspecJsonRenderer(), XmlStrictStubRenderer())
    responses = (
        ResponseSpec(ErrorModel, status_code=HTTPStatus.BAD_REQUEST),
        ResponseSpec(
            ErrorModel,
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        ResponseSpec(
            ErrorModel,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        ),
    )

    @modify(
        status_code=HTTPStatus.OK,
        operation_id="addPet",
        tags=["pet"],
        summary="Add a new pet to the store.",
        description="Add a new pet to the store.",
    )
    def post(self) -> Pet:
        # TODO: replace echo behavior with persistence-backed create logic.
        return self.parsed_body


class FindPetsByStatusBlueprint(
    Query[FindPetsByStatusQuery],
    Blueprint[PydanticSerializer],
):
    auth = _PET_AUTH
    renderers = (MsgspecJsonRenderer(), XmlStrictStubRenderer())
    responses = (
        ResponseSpec(ErrorModel, status_code=HTTPStatus.BAD_REQUEST),
        ResponseSpec(
            ErrorModel,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        ),
    )

    @modify(
        operation_id="findPetsByStatus",
        tags=["pet"],
        summary="Finds Pets by status.",
        description=(
            "Multiple status values can be provided with comma "
            "separated strings."
        ),
    )
    def get(self) -> list[Pet]:
        return []


class FindPetsByTagsBlueprint(
    Query[FindPetsByTagsQuery],
    Blueprint[PydanticSerializer],
):
    auth = _PET_AUTH
    renderers = (MsgspecJsonRenderer(), XmlStrictStubRenderer())
    responses = (
        ResponseSpec(ErrorModel, status_code=HTTPStatus.BAD_REQUEST),
        ResponseSpec(
            ErrorModel,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        ),
    )

    @modify(
        operation_id="findPetsByTags",
        tags=["pet"],
        summary="Finds Pets by tags.",
        description=(
            "Multiple tags can be provided with comma separated strings. "
            "Use tag1, tag2, tag3 for testing."
        ),
    )
    def get(self) -> list[Pet]:
        return []


class GetPetByIdBlueprint(
    Path[PetIdPath],
    Blueprint[PydanticSerializer],
):
    auth = _PET_AUTH_OR_API_KEY
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
        operation_id="getPetById",
        tags=["pet"],
        summary="Find pet by identifier.",
        description="Returns a single pet.",
    )
    def get(self) -> Pet:
        return Pet(
            id=self.parsed_path.petId,
            name="placeholder-pet",
            photoUrls=[],
        )


class UpdatePetWithFormBlueprint(
    Path[PetIdPath],
    Query[UpdatePetWithFormQuery],
    Blueprint[PydanticSerializer],
):
    auth = _PET_AUTH

    @validate(
        ResponseSpec(
            None,
            status_code=HTTPStatus.OK,
            limit_to_content_types=_NO_BODY_CONTENT_TYPE,
        ),
        ResponseSpec(ErrorModel, status_code=HTTPStatus.BAD_REQUEST),
        ResponseSpec(
            ErrorModel,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        ),
        validate_responses=False,
        operation_id="updatePetWithForm",
        tags=["pet"],
        summary="Updates a pet in the store with form data.",
        description="update a pet via the form data.",
    )
    def post(self) -> HttpResponse:
        # TODO: implement update side effects.
        return HttpResponse(status=HTTPStatus.OK)


class DeletePetBlueprint(
    Path[PetIdPath],
    Headers[DeletePetHeaders],
    Blueprint[PydanticSerializer],
):
    auth = _PET_AUTH

    @validate(
        ResponseSpec(
            None,
            status_code=HTTPStatus.OK,
            limit_to_content_types=_NO_BODY_CONTENT_TYPE,
        ),
        ResponseSpec(ErrorModel, status_code=HTTPStatus.BAD_REQUEST),
        ResponseSpec(
            ErrorModel,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        ),
        validate_responses=False,
        operation_id="deletePet",
        tags=["pet"],
        summary="Deletes a pet.",
        description="delete a pet.",
    )
    def delete(self) -> HttpResponse:
        # TODO: implement deletion.
        return HttpResponse(status=HTTPStatus.OK)


class UploadFileBlueprint(
    Path[PetIdPath],
    Query[UploadFileQuery],
    Body[bytes],
    Blueprint[PydanticSerializer],
):
    auth = _PET_AUTH
    parsers = (OctetStreamStrictStubParser(),)
    renderers = (MsgspecJsonRenderer(),)
    responses = (
        ResponseSpec(
            ErrorModel,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        ),
    )

    @modify(
        status_code=HTTPStatus.OK,
        operation_id="uploadFile",
        tags=["pet"],
        summary="Uploads an image.",
        description="Upload an image of pet.",
    )
    def post(self) -> ApiResponse:
        return ApiResponse(
            code=200,
            type="stub",
            message="Upload stub accepted for transport skeleton.",
        )
