from typing import TYPE_CHECKING, Any

from typing_extensions import override

from dmr.openapi.objects import Components, OAuthFlow, OAuthFlows, SecurityScheme
from dmr.openapi.objects.security_requirement import SecurityRequirement
from dmr.security import SyncAuth

if TYPE_CHECKING:
    from dmr.controller import Controller
    from dmr.endpoint import Endpoint
    from dmr.serializer import BaseSerializer


class PetstoreOAuthSyncAuth(SyncAuth):
    __slots__ = ("_scopes",)

    def __init__(self, scopes: tuple[str, ...] = ()) -> None:
        self._scopes = scopes

    @property
    @override
    def security_scheme(self) -> Components:
        return Components(
            security_schemes={
                "petstore_auth": SecurityScheme(
                    type="oauth2",
                    flows=OAuthFlows(
                        implicit=OAuthFlow(
                            authorization_url=(
                                "https://petstore3.swagger.io/oauth/authorize"
                            ),
                            scopes={
                                "write:pets": "modify pets in your account",
                                "read:pets": "read your pets",
                            },
                        ),
                    ),
                ),
            },
        )

    @property
    @override
    def security_requirement(self) -> SecurityRequirement:
        return {"petstore_auth": list(self._scopes)}

    @override
    def __call__(
        self,
        endpoint: "Endpoint",
        controller: "Controller[BaseSerializer]",
    ) -> Any | None:
        # TODO: replace permissive stub with real OAuth2 validation.
        return True


class ApiKeyHeaderSyncAuth(SyncAuth):
    __slots__ = ()

    @property
    @override
    def security_scheme(self) -> Components:
        return Components(
            security_schemes={
                "api_key": SecurityScheme(
                    type="apiKey",
                    name="api_key",
                    security_scheme_in="header",
                ),
            },
        )

    @property
    @override
    def security_requirement(self) -> SecurityRequirement:
        return {"api_key": []}

    @override
    def __call__(
        self,
        endpoint: "Endpoint",
        controller: "Controller[BaseSerializer]",
    ) -> Any | None:
        # TODO: replace permissive stub with real API key validation.
        return True
