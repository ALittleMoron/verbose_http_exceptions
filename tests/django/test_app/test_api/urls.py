from django.urls import path

from .views import ExceptionView, NoPermissionView, TestView

urlpatterns = [
    path("test", TestView.as_view({"post": "create"})),
    path("test/<int:pk>", TestView.as_view({"get": "retrieve"})),
    path("denied", NoPermissionView.as_view({"get": "list"})),
    path("exception", ExceptionView.as_view()),
]
