import json
import re

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

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
        
        elif mobile_number:
            print(mobile_number_form.match(mobile_number))
            if not mobile_number_form.match(mobile_number):
               return JsonResponse({'MESSAGE':'INVALID_MOBILE_NUMBER'}, status=400)
            elif User.objects.filter(mobile_number = data['mobile_number']):
               return JsonResponse({'MESSAGE':'ALREADY_EXISTS'}, status=400)

        elif email:
           if not email_form.match(str(email)):
               return JsonResponse({'MESSAGE':'INVALID_EMAIL'}, status=400)
           elif User.objects.filter(email = data['email']):
               return JsonResponse({'MESSAGE':'ALREADY_EXISTS'}, status=400)
        
        # if mobile_number:
        #     if '-' in data['mobile_number']:
        #         return JsonResponse({'MESSAGE':'INVALID_MOBILE_NUMBER'}, status=400)
        #     if User.objects.filter(mobile_number = data['mobile_number']):
        #         return JsonResponse({'MESSAGE':'ALREADY_EXISTS'}, status=400)
        
        # if email:
        #     if ('@' or '.') not in data['email']:
        #         return JsonResponse({'MESSAGE':'INVALID_EMAIL'}, status=400)
        #     if User.objects.filter(email = data['email']):
        #         return JsonResponse({'MESSAGE':'ALREADY_EXISTS'}, status=400)

        
        if User.objects.filter(user_name = data['user_name']):
            return JsonResponse({'MESSAGE':'ALREADY_EXISTS'}, status=400)

        
        if len(data['password']) < PASSWORD_MINIMUM_LENGTH:
            return JsonResponse({'MESSAGE':'PASSWORD_VALIDATION_ERROR'}, status=400)

        print(email)

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
        login_id      = data.get('id', None)
        #mobile_number = data.get('mobile_number', None)
        #email         = data.get('email', None)
        password      = data.get('password', None)

        #if not login_id or password:
        #    return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        #if User.objects.filter(mobile_number = mobile_number).exists():
        #    user = User.objects.get(mobile_number = data['mobile_number'])
        #    if user.password == password:
        #        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        #    else:
        #        return JsonResponse({'MESSAGE':'PASSWORD_ERROR'}, status=401)
        #else:
        #    return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

        #if User.objects.filter(email = email).exists():
        #    user = User.objects.get(email = data['email'])
        #    if user.password == password:
        #        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        #    else:
        #        return JsonResponse({'MESSAGE':'PASSWORD_ERROR'}, status=401)
        #else:
        #    return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

        if not login_id or password:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        else :
            if not User.objects.filter(
                    Q(mobile_number = login_id) |
                    Q(email = login_id) |
                    Q(user_name = login_id)
                    ).exists():
                return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)
            user = User.objects.get(
                    Q(mobile_number = data['mobile_number'])|
                    Q(email = data['email']) |
                    Q(user_name = login_id)
                    )
            if user.password != password:
                return JsonResponse({'MESSAGE':'PASSWORD_ERROR'}, status=401)
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

