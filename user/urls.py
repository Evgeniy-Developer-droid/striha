from django.urls import path
from .views import *

urlpatterns = [
    path('<str:key>', UserPublicView.as_view(), name="user-public"),
]