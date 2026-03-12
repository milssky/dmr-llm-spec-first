import pydantic


class PetIdPath(pydantic.BaseModel):
    petId: int


class FindPetsByStatusQuery(pydantic.BaseModel):
    status: str = "available"


class FindPetsByTagsQuery(pydantic.BaseModel):
    tags: list[str] | None = None


class UpdatePetWithFormQuery(pydantic.BaseModel):
    name: str | None = None
    status: str | None = None


class DeletePetHeaders(pydantic.BaseModel):
    api_key: str | None = None


class UploadFileQuery(pydantic.BaseModel):
    additionalMetadata: str | None = None
