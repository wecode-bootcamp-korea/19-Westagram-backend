from django.views import View

from .models import Posts
from .auth   import loginauth


class PostView(View):
    @loginauth
    def post(self, request):
        pass
    
    @loginauth
    def get(self, request):
        pass
    
    @loginauth
    def edit(self, request):
        pass