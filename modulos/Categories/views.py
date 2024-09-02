from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.views.generic import DetailView, ListView

from modulos.Authorization import permissions
from modulos.Categories.decorators import permissions_required
from modulos.Categories.forms import CategoryCreationForm
from modulos.Categories.models import Category
from modulos.Posts.models import Post


class CategoryCreateView(generic.CreateView):
    form_class = CategoryCreationForm
    template_name = "create_category.html"
    success_url = "/categories/"


class CategoryListView(ListView):
    model = Category
    template_name = "categories_list.html"
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    model = Category
    template_name = (
        "category_detail.html"  # Asegúrate de tener un template con este nombre
    )
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aquí puedes agregar más información al contexto si es necesario
        return context


# Vista para crear categorias
@login_required
@permissions_required([permissions.CATEGORY_MANAGE_PERMISSION])
def category_create(request):
    if request.method == "POST":
        form = CategoryCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("category_list")
    else:
        form = CategoryCreationForm()
    context = {"form": form}
    return render(request, "category_form.html", context)


# Vista para listar categorias
@login_required
@permissions_required([permissions.CATEGORY_MANAGE_PERMISSION])
def category_list(request):
    categories = Category.objects.all()
    return render(request, "category_list.html", {"categories": categories})


# Vista para eliminar una categoría
@login_required
@permissions_required([permissions.CATEGORY_MANAGE_PERMISSION])
def category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == "POST":
        # Verifica si hay posts asociados a esta categoría
        if Post.objects.filter(category=category).exists():
            # Mostrar un mensaje de error si hay posts asociados
            return render(
                request,
                "category_confirm_delete.html",
                {
                    "category": category,
                    "error_message": "No se puede eliminar la categoría porque tiene posts asociados.",
                },
            )

        # Elimina la categoría si no hay posts asociados
        category.delete()
        return redirect("category_list")
    return render(request, "category_confirm_delete.html", {"category": category})


# Vista para editar un usuario existente
@login_required
@permissions_required([permissions.CATEGORY_MANAGE_PERMISSION])
def category_edit(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == "POST":
        form = CategoryCreationForm(request.POST, instance=category)
        if form.is_valid():
            # Verifica si la categoría está siendo cambiada a inactiva y tiene posts asociados
            if (
                form.cleaned_data["status"] == "INACTIVO"
                and Post.objects.filter(category=category).exists()
            ):
                return render(
                    request,
                    "category_form.html",
                    {
                        "form": form,
                        "error_message": "No se puede inactivar la categoría porque tiene posts asociados.",
                    },
                )
            form.save()
            return redirect("category_list")
    else:
        form = CategoryCreationForm(instance=category)
    return render(request, "category_form.html", {"form": form})
