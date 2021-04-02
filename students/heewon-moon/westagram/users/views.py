import re
import json

from django.views           import View
from django.http            import JsonResponse

from .models                import User


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email       = data['email']
            password    = data['password']
            nickname    = data['nickname']
            phone       = data['phone']

            
            email_pattern       = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            email_is_valid      = re.compile(email_pattern)
            email_check         = email_is_valid.match(email)

            password_pattern    = '^([^\s])(?=.*[A-Z])(?=.*[!@#$&*?])(?=.*[0-9])(?=.*[a-z])([^\s])*$'
            password_is_valid   = re.compile(password_pattern)
            password_check      = password_is_valid.match(password)

            phone_is_valid      = re.compile('\d{9,11}')
            phone_check         = phone_is_valid.match(phone)


            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE' : 'EMAIL ALREADY EXISTS'}, status=400)

            if not email_check:
                return JsonResponse({'MESSAGE' : 'INVALID EMAIL'}, status=400) 

            if not password_check:
                return JsonResponse({'MESSAGE' : 'INVALID PASSWORD'}, status=400)

            if not phone_check:
                return JsonResponse({'MESSAGE' : 'INVALID PHONE NUMBER'}, status=400)


            User.objects.create(
                email       = email,
                password    = password,
                nickname    = nickname,
                phone       = phone
            )

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)
        else:
            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=400)

        