from django.urls import path

from user.views  import SignUp

urlpatterns = [
    path('/signup', SignUp.as_view()),
]