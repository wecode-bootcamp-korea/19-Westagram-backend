import json
import re

from django.http  import JsonResponse
from django.views import View

from users.models import User

PASSWORD_MINIMUM_LENGTH = 8

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        mobile_number = data.get('mobile_number', None)
        email         = data.get('email', None)
        name          = data.get('name', None)
        user_name     = data.get('user_name', None)
        password      = data.get('password', None)
        
        mobile_number_form = re.compile('[0-9]{3}-[0-9]{3,4}-[0-9]{4}')
        email_form         = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

        if not (
                (mobile_number or email)
                and name
                and user_name
                and password
                ):
            return JsonResponse({'MESSAGE':'INVALID_KEY'}, status=400)
        
        if mobile_number:
            if not mobile_number_form.match(mobile_number):
                return JsonResponse({'MESSAGE':'INVALID_MOBILE_NUMBER'}, status=400)
            if User.objects.filter(mobile_number = mobile_number).exists():
                return JsonResponse({'MESSAGE':'ALREADY_EXISTS'}, status=400)

        if email:
            if not email_form.match(email):
                return JsonResponse({'MESSAGE':'INVALID_EMAIL'}, status=400)
            if User.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE':'ALREADY_EXISTS'}, status=400)
        
        if User.objects.filter(user_name = user_name).exists():
            return JsonResponse({'MESSAGE':'ALREADY_EXISTS'}, status=400)

        
        if len(data['password']) < PASSWORD_MINIMUM_LENGTH:
            return JsonResponse({'MESSAGE':'PASSWORD_VALIDATION_ERROR'}, status=400)

        User.objects.create(
                mobile_number = mobile_number,
                email = email,
                name = name,
                user_name = user_name,
                password = password,
                )

        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        password      = data.get('password', None)
        mobile_number = data.get('mobile_number', None)
        email = data.get('email', None)
        user_name = data.get('user_name', None)

        user_queryset = User.objects.filter(password=password)

        if not ((mobile_number or email or user_name) and password):
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        
        if user_queryset.exists():
            if mobile_number:
                if not User.objects.filter(mobile_number = mobile_number) or not User.objects.filter(password=password):
                    return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)
                else:
                    return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
            if email:
                if not User.objects.filter(email= email) or not User.objects.filter(password=password):
                    return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)
                else:
                    return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
            if user_name:
                if not User.objects.filter(user_name = user_name) or not User.objects.filter(password = password):
                    return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)
                else:
                    return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        else:
            return JsonResponse({'MESSAGE':'PASSWORD_ERROR'}, status=401)
