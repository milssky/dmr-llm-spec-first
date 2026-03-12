from django.urls import path

from dmr.routing import Router, compose_blueprints

from server.apps.pet import views

router = Router(
    [
        path(
            "pet",
            compose_blueprints(
                views.UpdatePetBlueprint,
                views.AddPetBlueprint,
            ).as_view(),
            name="pet_root",
        ),
        path(
            "pet/findByStatus",
            compose_blueprints(
                views.FindPetsByStatusBlueprint,
            ).as_view(),
            name="find_pets_by_status",
        ),
        path(
            "pet/findByTags",
            compose_blueprints(
                views.FindPetsByTagsBlueprint,
            ).as_view(),
            name="find_pets_by_tags",
        ),
        path(
            "pet/<int:petId>",
            compose_blueprints(
                views.GetPetByIdBlueprint,
                views.UpdatePetWithFormBlueprint,
                views.DeletePetBlueprint,
            ).as_view(),
            name="pet_by_id",
        ),
        path(
            "pet/<int:petId>/uploadImage",
            compose_blueprints(
                views.UploadFileBlueprint,
            ).as_view(),
            name="upload_file",
        ),
    ],
    prefix="",
)
