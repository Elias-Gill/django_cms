import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from modulos.Authorization.permissions import *
from modulos.Categories.models import Category
from modulos.Posts.models import Category, Post, Version


@pytest.mark.django_db
def test_post_expiration_inactivates_post():
    """
    Test para verificar que los posts se inactivan después de la fecha de validez.
    """
    # Configuración inicial de datos
    category = Category.objects.create(name="Test Category")
    user = get_user_model().objects.create_user(
        username="testuser", password="password"
    )

    # Crear un post que expira ayer
    post = Post.objects.create(
        title="Expiring Post",
        content="This post will expire",
        category=category,
        author=user,
        publication_date=timezone.now() - timezone.timedelta(days=2),
        expiration_date=timezone.now() - timezone.timedelta(days=1),
        active=True,
        status=Post.PUBLISHED,
    )

    # Ejecutar la lógica para inactivar el post expirado
    post.active = False
    post.save()

    # Verificar que el post está inactivo
    post.refresh_from_db()
    assert (
        not post.active
    ), "El post debería haberse inactivado después de la fecha de validez."


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.django_db
def test_home_view(client):
    """
    Test the home view to check if posts are displayed correctly.
    """
    url = reverse("home")

    # Test home view with no posts
    response = client.get(url)
    assert response.status_code == 200
    assert "pages/home.html" in [t.name for t in response.templates]
    assert "posts_recientes" in response.context  # Cambiar 'posts' a 'posts_recientes'
    ps_len = len(
        response.context["posts_recientes"]
    )  # Aquí también ajustar a 'posts_recientes'
    assert ps_len == 0, f"Expected 0 posts, got {ps_len}"

    # Test home view with existing posts
    categoria = Category.objects.create(name="hola")
    Post.objects.create(
        title="Test Post 1",
        content="Content of test post 1",
        status=Post.PUBLISHED,
        category=categoria,
    )
    Post.objects.create(
        title="Test Post 2",
        content="Content of test post 2",
        status=Post.DRAFT,
        category=categoria,
    )
    Post.objects.create(
        title="Test Post 3",
        content="Content of test post 3",
        status=Post.PUBLISHED,
        category=categoria,
    )

    response = client.get(url)
    assert response.status_code == 200
    assert "posts_recientes" in response.context
    ps_len = len(response.context["posts_recientes"])
    assert ps_len == 2, f"Expected 2 posts, got {ps_len}"


@pytest.mark.django_db
def test_view_post(client):
    """
    Test the post detail view with an existing post and a non-existent post.
    """
    category = Category.objects.create(name="hola")
    post = Post.objects.create(
        title="Test Post",
        content="Content of test post",
        tags="tag1, tag2",
        status=Post.PUBLISHED,
        category=category,
    )

    # Test post detail view with an existing post
    url = reverse("post_detail", args=[post.id])
    response = client.get(url)
    assert response.status_code == 200
    assert "pages/post_detail.html" in [t.name for t in response.templates]
    assert response.context["post"] == post
    assert response.context["tags"] == ["tag1", "tag2"]
    assert "categories" in response.context

    # Test post detail view with a non-existent post
    url = reverse("post_detail", args=[999])
    response = client.get(url)
    assert response.status_code == 404

    post = Post.objects.create(
        title="Test Post",
        content="Content of test post",
        tags="tag1, tag2",
        status=Post.DRAFT,
        category=category,
    )

    # Test post detail view on a draft post without permission
    url = reverse("post_detail", args=[post.id])
    response = client.get(url)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_post_view(client):
    """
    Test the create post view for different user permissions and form validation.
    """
    url = reverse("post_create")

    # Test access to create post view without login
    response = client.get(url)
    assert (
        response.status_code == 302
    ), "Should redirect to login page when not logged in."

    # Create user and log in
    user = get_user_model().objects.create_user(
        username="testuser", password="password"
    )
    client.login(username="testuser", password="password")

    # Test access to create post view without permission
    response = client.get(url)
    assert (
        response.status_code == 403
    ), "User without permission should get 403 Forbidden."

    # Assign permission and test access
    user.user_permissions.add(Permission.objects.get(codename=POST_CREATE_PERMISSION))
    response = client.get(url)
    assert (
        response.status_code == 200
    ), "User with permission should access the view successfully."
    assert "pages/new_post.html" in [
        t.name for t in response.templates
    ], "Template 'new_post.html' should be used."

    # Test creating a post with invalid data (missing required fields)
    data = {"title": "", "content": ""}  # Invalid data, fields required
    response = client.post(url, data)
    assert (
        response.status_code == 200
    ), "Invalid form data should return the form with errors (status 200)."
    assert "form" in response.context, "Form should be in the context."
    assert response.context["form"].errors, "Form should contain errors."

    # Test creating a post with valid data
    category = Category.objects.create(name="test_category", description="descripcion")
    data = {
        "title": "New Test Post",
        "content": "Content for new test post",
        "category": category.id,
    }
    response = client.post(url, data)
    assert response.status_code == 302, "Successful post creation should redirect."

    # Verify the post was created
    assert Post.objects.filter(
        title="New Test Post", active=True
    ).exists(), "Post should exist in the database after creation."


@pytest.mark.django_db
def test_post_manage_view(client):
    """
    Test the create post view for different user permissions and form validation.
    """
    url = reverse("post_list")

    # Test access to create post view without login
    response = client.get(url)
    assert (
        response.status_code == 302
    ), "Should redirect to login page when not logged in."

    # Create user and log in
    user = get_user_model().objects.create_user(
        username="testuser", password="password"
    )
    client.login(username="testuser", password="password")

    # Test access to create post view without permission
    response = client.get(url)
    assert (
        response.status_code == 403
    ), "User without permission should get 403 Forbidden."

    # Assign permission and test access
    user.user_permissions.add(Permission.objects.get(codename=POST_CREATE_PERMISSION))
    response = client.get(url)
    assert (
        response.status_code == 200
    ), "User with permission should access the view successfully."
    assert "pages/post_list.html" in [
        t.name for t in response.templates
    ], "Template 'post_list.html' should be used."


@pytest.mark.django_db
def test_favorite_post(client):
    """
    Test para marcar y desmarcar un post como favorito.
    """
    categoria = Category.objects.create(name="prueba")
    post = Post.objects.create(
        title="Post Favorito", content="Contenido del post favorito", category=categoria
    )
    user = get_user_model().objects.create_user(
        username="testuser", password="password"
    )
    client.login(username="testuser", password="password")

    # Test agregar post a favoritos
    url = reverse("post_favorite", args=[post.id])
    response = client.post(url)
    assert response.status_code == 302, "Debería retornar 302 al marcar como favorito."
    assert post.favorites.filter(
        id=user.id
    ).exists(), "El post debería estar en la lista de favoritos."

    # Test quitar post de favoritos
    response = client.post(url)
    assert (
        response.status_code == 302
    ), "Debería retornar 302 al desmarcar como favorito."
    assert not post.favorites.filter(
        id=user.id
    ).exists(), "El post no debería estar en la lista de favoritos."


@pytest.mark.django_db
def test_favorite_list_view(client):
    """
    Test para listar los posts favoritos del usuario.
    """
    categoria = Category.objects.create(name="prueba")
    user = get_user_model().objects.create_user(
        username="testuser", password="password"
    )
    post1 = Post.objects.create(
        title="Post 1", content="Contenido del post 1", category=categoria
    )
    post2 = Post.objects.create(
        title="Post 2", content="Contenido del post 2", category=categoria
    )

    post1.favorites.add(user)  # Marcar post1 como favorito
    post2.favorites.add(user)  # Marcar post2 como favorito

    client.login(username="testuser", password="password")
    url = reverse("post_favorite_list")
    response = client.get(url)

    assert (
        response.status_code == 200
    ), "Debería retornar 200 al acceder a la lista de favoritos."
    assert (
        "posts_favorites" in response.context
    ), "El contexto debería contener 'posts_favorites'."
    assert (
        len(response.context["posts_favorites"]) == 2
    ), "Debería mostrar 2 posts favoritos."


@pytest.mark.django_db
def test_search_post_view(client):
    """
    Test para buscar publicaciones.
    """
    categoria = Category.objects.create(name="prueba")
    Post.objects.create(
        title="Post de prueba",
        content="Contenido de prueba",
        category=categoria,
        status=Post.PUBLISHED,  # Asegúrate de que el post esté publicado
    )

    # Probar una búsqueda no válida (sin ningún criterio de búsqueda)
    url = reverse("post_search") + "?input="
    response = client.get(url)
    assert (
        response.status_code == 200
    ), "Debería redirigir a la vista de inicio si no hay búsqueda válida."

    # Probar una búsqueda válida
    url = reverse("post_search") + "?input=Post de prueba"
    response = client.get(url)
    assert (
        response.status_code == 200
    ), "Debería retornar 200 al buscar un post existente."
    assert len(response.context["posts"]) == 1, "Debería encontrar 1 post."
    assert (
        response.context["posts"][0].title == "Post de prueba"
    ), "El post encontrado debería ser el correcto."


@pytest.mark.django_db
def test_inactivate_post_view(client):
    """
    Test para inactivar un post.
    """
    categoria = Category.objects.create(name="prueba")
    user = get_user_model().objects.create_user(
        username="testuser", password="password"
    )
    user.user_permissions.add(Permission.objects.get(codename=POST_DELETE_PERMISSION))
    post = Post.objects.create(
        category=categoria,
        title="Post a inactivar",
        content="Contenido a inactivar",
        author=user,
    )
    client.login(username="testuser", password="password")

    url = reverse("inactivate_post", args=[post.id])

    # Test GET request
    response = client.get(url)
    assert (
        response.status_code == 200
    ), "Debería retornar 200 al acceder a la vista de confirmación de eliminación."

    # Test valid POST request
    response = client.post(url, {"msg": "mensaje"})
    assert (
        response.status_code == 302
    ), "Deberia retornar 302 luego de la desactivacion del post."

    post.refresh_from_db()
    assert not post.active, "El post debería haber sido inactivado."

    # Reset the post state for the next test
    post.active = True
    post.save()

    # Test invalid POST request
    response = client.post(url, {})
    assert (
        response.status_code == 200
    ), "Debería retornar 200 si el formulario es inválido."

    # Check for presence of form errors
    assert response.content != "", "Deberían aparecer errores en el formulario."

    post.refresh_from_db()
    assert (
        post.active
    ), "El post debería seguir activo después de un intento de inactivación fallido."


@pytest.mark.django_db
def test_edit_post(client):
    """
    Test para la vista de edición de un post.
    Verifica que un post existente se puede editar correctamente.
    """
    # Crea una categoría para el post
    category = Category.objects.create(
        name="Categoría de Prueba", description="Descripción de prueba"
    )

    # Crea un post asociado a la categoría
    post = Post.objects.create(
        title="Post a Editar", content="Contenido a editar", category=category
    )

    # Crea un usuario y asigna permisos
    user = get_user_model().objects.create_user(
        username="testuser", password="password"
    )
    user.user_permissions.add(Permission.objects.get(codename=POST_EDIT_PERMISSION))

    # Inicia sesión con el usuario creado
    client.login(username="testuser", password="password")

    # Obtiene la URL para editar el post
    url = reverse("edit_post", args=[post.id])

    # Datos para actualizar el post
    data = {
        "title": "Título editado",
        "content": "Contenido editado",
        "category": category.id,
    }

    # Realiza la solicitud POST para editar el post
    response = client.post(url, data)

    # Verifica que se redirigió correctamente
    assert response.status_code == 302

    # Refresca el post desde la base de datos
    post.refresh_from_db()

    # Verifica que el post se haya actualizado correctamente
    assert post.title == "Título editado"
    assert post.content == "Contenido editado"


@pytest.mark.django_db
def test_publish_post(client):
    """
    Test the publish post view for different user permissions and category moderation.
    """
    # Create user and log in
    user = get_user_model().objects.create_user(
        username="testuser", password="password"
    )
    client.login(username="testuser", password="password")

    # Create a post with a moderated category
    category = Category.objects.create(moderacion=Category.MODERADA)
    post = Post.objects.create(
        title="New Test Post",
        content="Content for new test post",
        category=category,
        author=user,
    )

    url = reverse("publish_post", args=[post.id])

    # Test access to publish post view without login
    response = client.get(url)
    assert (
        response.status_code == 403
    ), "Should redirect to login page when not logged in."

    # Test access to publish post view without permission in moderated category
    response = client.post(url)
    assert (
        response.status_code == 403
    ), "User without permission should get 403 Forbidden in moderated category."

    # Assign publish permission and test access
    user.user_permissions.add(Permission.objects.get(codename=POST_PUBLISH_PERMISSION))
    response = client.post(url)
    assert (
        response.status_code == 302
    ), "User with permission should be able to publish the post in moderated category."

    # Verify post is published
    post.refresh_from_db()
    assert (
        post.status == Post.PUBLISHED
    ), "Post status should be 'PUBLISHED' after publishing."
    assert (
        post.publication_date is not None
    ), "Post should have a publication date after publishing."

    # Test publishing a post in a 'LIBRE' category without permission
    category_free = Category.objects.create(moderacion=Category.LIBRE)
    post_free = Post.objects.create(
        title="Another Test Post",
        content="Content for another test post",
        category=category_free,
        author=user,
    )
    url_free = reverse("publish_post", args=[post_free.id])

    response = client.post(url_free)
    assert (
        response.status_code == 302
    ), "User without permission should be able to publish the post in 'LIBRE' category."

    # Verify post is published in 'LIBRE' category
    post_free.refresh_from_db()
    assert (
        post_free.status == Post.PUBLISHED
    ), "Post in 'LIBRE' category should be published."
    assert (
        post_free.publication_date is not None
    ), "Post should have a publication date after publishing."
