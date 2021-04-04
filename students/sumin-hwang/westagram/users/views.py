import json
#import re

from django.http import JsonResponse
from django.views import View
#from django.db.models import Q

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
        
        #mobile_number_form = re.compile('[0-9]{3}-[0-9]{4}-[0-9]{4}', mobile_number)
        #email_form         = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)

        if not (
                (mobile_number or email)
                and name
                and user_name
                and password
                ):
            return JsonResponse({'MESSAGE':'INVALID_KEY'}, status=400)
        
        #if mobile_number:
        #    if not mobile_number_form.match(str(mobile_number_form), mobile_number):
        #        return JsonResponse({'MESSAGE':'INVALID_MOBILE_NUMBER'}, status=400)

        #if email:
        #    if not email_form.match(str(email_form), email):
        #        return JsonResponse({'MESSAGE':'INVALID_EMAIL'}, status=400)
        
        if mobile_number:
            if '-' in data['mobile_number']:
                return JsonResponse({'MESSAGE':'INVALID_MOBILE_NUMBER'}, status=400)
            if User.objects.filter(mobile_number = data['mobile_number']):
                return JsonResponse({'MESSAGE':'ALREADY_EXISTS'}, status=400)
        
        if email:
            if ('@' or '.') not in data['email']:
                return JsonResponse({'MESSAGE':'INVALID_EMAIL'}, status=400)
            if User.objects.filter(email = data['email']):
                return JsonResponse({'MESSAGE':'ALREADY_EXISTS'}, status=400)
        
        if User.objects.filter(user_name = data['user_name']):
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
        mobile_number = data.get('mobile_number', None)
        email         = data.get('email', None)
        password      = data.get('password', None)

        #if User.objects.filter(mobile_number = data['mobile_number']).exists():
        if User.password == data['password']:
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        else:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=401)
