from django.urls import path
from user.views import UserView

urlpatterns =[
    path('/users', UserView.as_view()),
]