from django.urls import path

from dmr.routing import Router, compose_blueprints

from server.apps.store import views

router = Router(
    [
        path(
            "store/inventory",
            compose_blueprints(
                views.GetInventoryBlueprint,
            ).as_view(),
            name="get_inventory",
        ),
        path(
            "store/order",
            compose_blueprints(
                views.PlaceOrderBlueprint,
            ).as_view(),
            name="place_order",
        ),
        path(
            "store/order/<int:orderId>",
            compose_blueprints(
                views.GetOrderByIdBlueprint,
                views.DeleteOrderBlueprint,
            ).as_view(),
            name="order_by_id",
        ),
    ],
    prefix="",
)
