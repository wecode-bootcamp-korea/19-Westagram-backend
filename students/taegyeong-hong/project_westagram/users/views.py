import json
from django.http import JsonResponse
from django.views import View
from .models import User

class SignupView(View):
    def post(self, request):
        requestpassword = 8
        
        try:

            data = json.loads(request.body)

            if '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'message':'email validation'},status=400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'DUPLICATED EMAIL'},status=400)
            if len(data['password']) <= requestpassword :
                return JsonResponse({'message':'INVALID PASSWORD'},status=400)

            User.objects.create(
                email =data['email'],
                password = data['password'],
                name= data['name'],
                phone_num =data['phone_num']
            )
            return JsonResponse({'message':'SUCCESS'},stats=201)


        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)


