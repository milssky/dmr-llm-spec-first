from django.urls import path

from dmr.routing import Router, compose_blueprints

from server.apps.user import views

router = Router(
    [
        path(
            "user",
            compose_blueprints(
                views.CreateUserBlueprint,
            ).as_view(),
            name="create_user",
        ),
        path(
            "user/createWithList",
            compose_blueprints(
                views.CreateUsersWithListInputBlueprint,
            ).as_view(),
            name="create_users_with_list_input",
        ),
        path(
            "user/login",
            compose_blueprints(
                views.LoginUserBlueprint,
            ).as_view(),
            name="login_user",
        ),
        path(
            "user/logout",
            compose_blueprints(
                views.LogoutUserBlueprint,
            ).as_view(),
            name="logout_user",
        ),
        path(
            "user/<str:username>",
            compose_blueprints(
                views.GetUserByNameBlueprint,
                views.UpdateUserBlueprint,
                views.DeleteUserBlueprint,
            ).as_view(),
            name="user_by_name",
        ),
    ],
    prefix="",
)
