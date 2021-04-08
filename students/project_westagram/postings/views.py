import json
from django.http.response import JsonResponse
from django.views import View

from .models import Posts
from .utils  import loginauth


class PostView(View):
    @loginauth
    def post(self, request):
        data = json.loads(request.body)
        
        return JsonResponse({'message': data}, status = 200)
    
    @loginauth
    def get(self, request):
        pass
    
    @loginauth
    def edit(self, request):
        pass