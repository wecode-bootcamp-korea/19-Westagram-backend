from django.urls import path

from user.views  import UsersView

urlpatterns = [
    path('/users', UsersView.as_view())
]