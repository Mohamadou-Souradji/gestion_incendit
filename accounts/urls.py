from django.urls import path

from .views import AppLoginView, app_logout, profile_view, user_list, user_create, user_edit, user_delete

app_name = "accounts"

urlpatterns = [
    path("login/", AppLoginView.as_view(), name="login"),
    path("logout/", app_logout, name="logout"),
    path("profil/", profile_view, name="profile"),
    path("utilisateurs/", user_list, name="user_list"),
    path("utilisateurs/nouveau/", user_create, name="user_create"),
    path("utilisateurs/<int:pk>/modifier/", user_edit, name="user_edit"),
    path("utilisateurs/<int:pk>/supprimer/", user_delete, name="user_delete"),
]
