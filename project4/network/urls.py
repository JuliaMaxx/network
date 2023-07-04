
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit",views.edit,name="edit"),
    path("edited/<int:id>", views.edited, name='edited'),
    path("likes/<int:id>/<int:user_id>", views.likes, name="likes"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:profile_id>",views.profile, name='profile'),
    path('following/<int:profile_id>', views.following, name='following')
]
