from django.urls import path
from users.views import Sign

urlpatterns = [
        path('/signin', Sign.as_view())
        ]
