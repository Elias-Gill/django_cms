from django.urls import path

from .views import payment_success, payment_view

urlpatterns = [
    path("pay/<int:category_id>/", payment_view, name="payment_view"),
    path("success/<int:category_id>/", payment_success, name="payment_success"),
]
