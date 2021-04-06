import json
from django.http import JsonResponse
from django.views import View
from .models import User
# Create your views here.

class SigninView(View):
    def post(self, request):
        data = json.loads(request.body)
    try :
        if User.objects.filter(name=data['user']).exists():


        

            name =data['name']
            password = data['password']
            
            
        if 
        return JsonResponse({'messae'})

