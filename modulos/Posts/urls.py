from django.urls import path

from .views import *

urlpatterns = [
    # -- vistas de usuario --
    path("admin", manage_posts, name="post_list"),
    path("inactives", manage_inactive_posts, name="inactives_list"),
    path("<int:id>/", view_post, name="post_detail"),
    path("search/", enhanced_search, name="post_search"),
    # -- administracion de contenido --
    path("create/", create_post, name="post_create"),
    path("<int:id>/inactivate", inactivate_post, name="inactivate_post"),
    path("<int:id>/reactivate", reactivate_post, name="reactivate_post"),
    path("<int:id>/edit/", edit_post, name="edit_post"),
    path("<int:id>/highlight/", highlight_post, name="highlight_post"),
    # -- vistas de publicacion de contenido --
    path("<int:id>/approve", aprove_post, name="approve_post"),
    path("<int:id>/review", send_to_review, name="send_to_review"),
    path("<int:id>/publish", publish_post, name="publish_post"),
    path("<int:id>/reject", reject_post, name="reject_post"),
    path("kanban/", kanban_board, name="kanban_board"),
    # -- historial --
    path("<int:id>/versions", post_versions_list, name="post_versions"),
    path(
        "<int:post_id>/versions/<int:version>/",
        post_version_detail,
        name="post_version_detail",
    ),
    path("<int:id>/logs", post_log_list, name="post_log_list"),
    path(
        "<int:post_id>/versions/<int:version>/revert",
        post_revert_version,
        name="post_revert_version",
    ),
    # -- estadisticas --
    path("<int:id>/statistics", post_statistics, name="post_statistics"),
    # -- miscelanea --
    path("<int:id>/add_favorite", favorite_post, name="post_favorite"),
    path("favorites", favorite_list, name="post_favorite_list"),
]
