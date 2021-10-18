
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    #my urls
    path("new", views.new_view, name="new"),
    path("profile", views.profile_view, name="profile"),
    path("following", views.following_view, name="following"),
    #API routes
    path('post/<int:id>',views.post,name="post"),
]
