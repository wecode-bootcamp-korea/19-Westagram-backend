import json

from django.http  import JsonResponse
from django.views import View

from .models  import User

class SignUpView(View):
    def post(self, request):
        PASSWORD_LENGTH = 8
        
        try:
            data = json.loads(request.body)

            if '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'MESSGAGE': 'INVALID EMAIL'}, status=400)
            
            if User.objects.filter(email= data['email']).exists():
                return JsonResponse({'MESSGAGE': 'DUPLICATED EMAIL'}, status=400)
            
            if len(data['password']) <= PASSWORD_LENGTH:
                return JsonResponse({'MESSGAGE': 'INVALID PASSWORD'}, status=400)
            
            User.objects.create(
                email        = data['email'],
                password     = data['password'],
                name         = data['name'],
                phone_number = data['phone_number']
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR'}, status=400)
