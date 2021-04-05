from django.urls import path
from user.views import SignupView

urlpatterns =[
    path('/users', SignupView.as_view()),
]
