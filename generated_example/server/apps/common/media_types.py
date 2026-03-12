from collections.abc import Callable
from typing import Any

from django.http import HttpRequest
from typing_extensions import override

from dmr.parsers import DeserializeFunc, Parser, Raw
from dmr.renderers import Renderer


class XmlStrictStubParser(Parser):
    __slots__ = ()

    content_type = "application/xml"

    @override
    def parse(
        self,
        to_deserialize: Raw,
        deserializer_hook: DeserializeFunc | None = None,
        *,
        request: HttpRequest,
        model: Any,
    ) -> Any:
        raise NotImplementedError(
            "XML parsing is intentionally stubbed in strict-stub mode.",
        )


class XmlStrictStubRenderer(Renderer):
    __slots__ = ()

    content_type = "application/xml"

    @override
    def render(
        self,
        to_serialize: Any,
        serializer_hook: Callable[[Any], Any],
    ) -> bytes:
        raise NotImplementedError(
            "XML rendering is intentionally stubbed in strict-stub mode.",
        )

    @property
    @override
    def validation_parser(self) -> XmlStrictStubParser:
        return XmlStrictStubParser()


class OctetStreamStrictStubParser(Parser):
    __slots__ = ()

    content_type = "application/octet-stream"

    @override
    def parse(
        self,
        to_deserialize: Raw,
        deserializer_hook: DeserializeFunc | None = None,
        *,
        request: HttpRequest,
        model: Any,
    ) -> Any:
        raise NotImplementedError(
            "application/octet-stream parsing is stubbed in strict-stub mode.",
        )
