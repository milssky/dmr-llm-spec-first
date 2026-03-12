from http import HTTPStatus

from django.http import HttpResponse

from dmr import Blueprint, Body, Path, ResponseSpec, modify, validate
from dmr.errors import ErrorModel
from dmr.parsers import FormUrlEncodedParser
from dmr.plugins.msgspec import MsgspecJsonParser, MsgspecJsonRenderer
from dmr.plugins.pydantic import PydanticSerializer

from server.apps.common.media_types import XmlStrictStubParser, XmlStrictStubRenderer
from server.apps.common.security import ApiKeyHeaderSyncAuth
from server.apps.common.serializers import Order
from server.apps.store.serializers import OrderIdPath

_API_KEY_AUTH = (ApiKeyHeaderSyncAuth(),)
_NO_BODY_CONTENT_TYPE = {"application/x.no-body"}


class GetInventoryBlueprint(Blueprint[PydanticSerializer]):
    auth = _API_KEY_AUTH
    responses = (
        ResponseSpec(
            ErrorModel,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        ),
    )

    @modify(
        operation_id="getInventory",
        tags=["store"],
        summary="Returns pet inventories by status.",
        description="Returns a map of status codes to quantities.",
    )
    def get(self) -> dict[str, int]:
        return {}


class PlaceOrderBlueprint(
    Body[Order],
    Blueprint[PydanticSerializer],
):
    parsers = (
        MsgspecJsonParser(),
        XmlStrictStubParser(),
        FormUrlEncodedParser(),
    )
    renderers = (MsgspecJsonRenderer(),)
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
        operation_id="placeOrder",
        tags=["store"],
        summary="Place an order for a pet.",
        description="Place a new order in the store.",
    )
    def post(self) -> Order:
        # TODO: implement order placement.
        return self.parsed_body


class GetOrderByIdBlueprint(
    Path[OrderIdPath],
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
        operation_id="getOrderById",
        tags=["store"],
        summary="Find purchase order by identifier.",
        description=(
            "For valid response try integer IDs with value <= 5 or > 10. "
            "Other values will generate exceptions."
        ),
    )
    def get(self) -> Order:
        return Order(
            id=self.parsed_path.orderId,
            petId=0,
            quantity=0,
        )


class DeleteOrderBlueprint(
    Path[OrderIdPath],
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
        operation_id="deleteOrder",
        tags=["store"],
        summary="Delete purchase order by identifier.",
        description=(
            "For valid response try integer IDs with value < 1000. "
            "Anything above 1000 or non-integers will generate API errors."
        ),
    )
    def delete(self) -> HttpResponse:
        # TODO: implement order deletion.
        return HttpResponse(status=HTTPStatus.OK)
