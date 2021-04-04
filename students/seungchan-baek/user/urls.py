from django.urls import path

from user.views  import SignUpView


urlpatterns = [
    path('/users', SignUpView.as_view())
]