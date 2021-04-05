from .views         import UserView, LoginView
from django.urls    import path

urlpatterns =[
        path('/signup', UserView.as_view()),
        path('/login', LoginView.as_view())
        ]
