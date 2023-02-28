from django.urls import path
from .api import *
from .views import *

urlpatterns = [
    path('profile/<str:key>', UserPublicView.as_view(), name="user-public"),

    # api
    path('change-avatar', change_avatar, name="change-avatar"),
    path('get-new-notification', get_new_notification, name="get-new-notification"),
    path('get-all-notification', get_all_notification, name="get-all-notification"),
    path('read-notification', read_notifications, name="read-notification"),
]