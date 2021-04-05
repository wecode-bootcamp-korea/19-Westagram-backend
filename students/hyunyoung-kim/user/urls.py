from django.urls import path

from user.views  import SignUp, SingIn

urlpatterns = [
    path('/signup', SignUp.as_view()),
    path('/signin', SingIn.as_view())
]