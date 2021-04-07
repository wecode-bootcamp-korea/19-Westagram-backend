import json
from django.http import JsonResponse
from django.views import View
from .models import User

class SignupView(View):
    def post(self, request):
        PASSWORD_NUM = 8
        try:
            data = json.loads(request.body)
            if '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'message':'email validation'},status=400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'DUPLICATED EMAIL'},status=400)

            if len(data['password']) <= PASSWORD_NUM :
                return JsonResponse({'message':'INVALID PASSWORD'},status=400)

            User.objects.create(
                email       = data['email'],
                password    = data['password'],
                name        = data['name'],
                phone_num   =data['phone_num']
            )
            return JsonResponse({'message':'SUCCESS'},stats=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)

class SigninView(View):
    def post(self, requests):


        try :
                        
            data    = json.loads(request.body)
            email   = data[email]
            pasword = data[password]
            user    = User.objects.get(email = data['email'])

            if  User.objects.filter(email=data['email']).exists() :
                    user = Account.objects.get(email=data['email'])  

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)
