from dmr.openapi import OpenAPIConfig
from dmr.openapi.objects import (
    Contact,
    ExternalDocumentation,
    License,
    Server,
    Tag,
)


def get_config() -> OpenAPIConfig:
    return OpenAPIConfig(
        title="Swagger Petstore - OpenAPI 3.1",
        version="1.0.12",
        description=(
            "This is a sample Pet Store Server based on the OpenAPI 3.1 "
            "specification. You can find out more about Swagger at "
            "https://swagger.io."
        ),
        terms_of_service="https://swagger.io/terms/",
        contact=Contact(email="apiteam@swagger.io"),
        license=License(
            name="Apache 2.0",
            url="https://www.apache.org/licenses/LICENSE-2.0.html",
        ),
        external_docs=ExternalDocumentation(
            description="Find out more about Swagger",
            url="https://swagger.io",
        ),
        servers=[Server(url="https://petstore31.swagger.io/api/v3")],
        tags=[
            Tag(
                name="pet",
                description="Everything about your Pets",
                external_docs=ExternalDocumentation(
                    description="Find out more",
                    url="http://swagger.io",
                ),
            ),
            Tag(
                name="store",
                description="Access to Petstore orders",
                external_docs=ExternalDocumentation(
                    description="Find out more about our store",
                    url="http://swagger.io",
                ),
            ),
            Tag(name="user", description="Operations about user"),
        ],
    )
