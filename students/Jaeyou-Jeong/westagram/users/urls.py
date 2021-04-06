from django.urls import path
from users.views import Sign

urlpatterns = [
        path('/signup', Sign.as_view())
        ]
