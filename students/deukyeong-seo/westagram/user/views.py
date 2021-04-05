import json

from django.views import View
from django.http  import JsonResponse

from .models import User

class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)

        try:    
        
            name     = data['name']
            email    = data['email']
            password = data['password']

            User.objects.create(name=name, email=email, password=password)

            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
