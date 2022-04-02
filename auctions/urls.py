from django.urls import path

from . import views

# app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("review/<str:lstpk>", views.listingreview, name="listingreview"),
    path("wlswitch/<str:lstpk>", views.wlswitch, name="wlswitch"),
    path("mylists/<str:listType>", views.mylists, name="mylists"),
    path("cat/<str:catpk>", views.cat, name="cat")
]
