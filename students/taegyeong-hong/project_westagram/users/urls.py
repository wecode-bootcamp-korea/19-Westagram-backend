from django.urls import path
from .views import SignupView



urlpatterns =[
        path('/users', SignupView.as_view()),
      #  path('/signin', SigninView.as_view())




        ]
