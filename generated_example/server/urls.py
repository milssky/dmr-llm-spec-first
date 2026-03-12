from django.urls import include, path

from dmr.openapi import build_schema
from dmr.openapi.views import OpenAPIJsonView, RedocView, ScalarView, SwaggerView
from dmr.routing import Router
from server.apps.pet import urls as pet_urls
from server.apps.store import urls as store_urls
from server.apps.user import urls as user_urls
from server.openapi_config import get_config

router = Router(
    [
        path(
            pet_urls.router.prefix,
            include((pet_urls.router.urls, "pet"), namespace="pet"),
        ),
        path(
            store_urls.router.prefix,
            include((store_urls.router.urls, "store"), namespace="store"),
        ),
        path(
            user_urls.router.prefix,
            include((user_urls.router.urls, "user"), namespace="user"),
        ),
    ],
    prefix="",
)

schema = build_schema(router, config=get_config())

urlpatterns = [
    path(router.prefix, include((router.urls, "server"), namespace="api")),
    path("docs/openapi.json/", OpenAPIJsonView.as_view(schema), name="openapi"),
    path("docs/redoc/", RedocView.as_view(schema), name="redoc"),
    path("docs/swagger/", SwaggerView.as_view(schema), name="swagger"),
    path("docs/scalar/", ScalarView.as_view(schema), name="scalar"),
]
