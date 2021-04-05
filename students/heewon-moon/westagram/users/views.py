import re
import json

from django.views import View
from django.http  import JsonResponse

from .models      import User
from .validators  import email_validator, password_validator, phone_validator


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email       = data['email']
            password    = data['password']
            nickname    = data['nickname']
            phone       = data['phone']


            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE' : 'EMAIL ALREADY EXISTS'}, status=400)

            if not email_validator(email):
                return JsonResponse({'MESSAGE' : 'INVALID EMAIL'}, status=400) 

            if not password_validator(password):
                return JsonResponse({'MESSAGE' : 'INVALID PASSWORD'}, status=400)

            if not phone_validator(phone):
                return JsonResponse({'MESSAGE' : 'INVALID PHONE NUMBER'}, status=400)

            User.objects.create(
                email       = email,
                password    = password,
                nickname    = nickname,
                phone       = phone
            )

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)


class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            account = data['account']
            password = data['password']


            if email_validator(account):
                user = User.objects.get(email=account)
            elif phone_validator(account):
                user = User.objects.get(phone=account)
            else:
                user = User.objects.get(nickname=account)
            

            if not user:
                return JsonResponse({'MESSSAGE' : 'INVALID USER'}, status=401)
            
            if user.password != password:
                return JsonResponse({'MESSAGE' : 'WRONG PASSWORD'}, status=401)
            

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)
        else:
            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)