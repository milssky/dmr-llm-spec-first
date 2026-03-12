from pathlib import Path

import yaml
from django.test import Client

ROOT = Path(__file__).resolve().parents[2]


def _source_spec() -> dict:
    with (ROOT / "openapi.yaml").open("r", encoding="utf-8") as spec_file:
        return yaml.safe_load(spec_file)


def _generated_spec() -> dict:
    response = Client().get("/docs/openapi.json/")
    assert response.status_code == 200
    return response.json()


def test_docs_endpoints_are_available() -> None:
    client = Client()
    assert client.get("/docs/openapi.json/").status_code == 200
    assert client.get("/docs/redoc/").status_code == 200
    assert client.get("/docs/swagger/").status_code == 200
    assert client.get("/docs/scalar/").status_code == 200


def test_openapi_contract_smoke_fidelity() -> None:
    source = _source_spec()
    generated = _generated_spec()

    assert generated["openapi"] == source["openapi"]
    assert generated["info"]["title"] == source["info"]["title"]
    assert generated["info"]["version"] == source["info"]["version"]

    assert set(generated["paths"]) == set(source["paths"])
    for path, source_item in source["paths"].items():
        assert set(generated["paths"][path]) == set(source_item)

    assert "petstore_auth" in generated["components"]["securitySchemes"]
    assert "api_key" in generated["components"]["securitySchemes"]

    login_200 = generated["paths"]["/user/login"]["get"]["responses"]["200"]
    assert "X-Rate-Limit" in login_200["headers"]
    assert "X-Expires-After" in login_200["headers"]

    get_pet_security = generated["paths"]["/pet/{petId}"]["get"]["security"]
    assert {"api_key": []} in get_pet_security
    assert {"petstore_auth": ["write:pets", "read:pets"]} in get_pet_security

    put_pet_media_types = generated["paths"]["/pet"]["put"]["requestBody"]["content"]
    assert "application/json" in put_pet_media_types
    assert "application/xml" in put_pet_media_types
    assert "application/x-www-form-urlencoded" in put_pet_media_types

    upload_media_types = generated["paths"]["/pet/{petId}/uploadImage"]["post"][
        "requestBody"
    ]["content"]
    assert "application/octet-stream" in upload_media_types
