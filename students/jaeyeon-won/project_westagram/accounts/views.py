import json
import re

from django.views import View
from django.http  import JsonResponse

from .models      import User

class SignupView(View):
    def post(self,request):
        data = json.loads(request.body)

        try:
            name                = data['name']
            phone_number        = data['phone_number']
            email               = data['email']
            username            = data ['username']
            password            = data['password']
            email_vaildation    = re.match('[a-zA-Z0-9._+-]+@[a-z0-9-]+\.[a-z.]+',email)
            password_vaildation = re.match('^(?=.*[a-zA-Z0-9.,-]).{8,}$',password)
            
            if name =='' or (phone_number=='' and email=='') or username == '' or password =='':
                return JsonResponse({'message' : 'Check your Input'}, status = 400)

            if not email_vaildation:
                return JsonResponse({'messsage' : 'Check your email'}, status = 400)

            if not password_vaildation:
                return JsonResponse({'message' : 'Check your password'}, status = 400)

            if User.objects.filter(phone_number = phone_number).exists():
                return JsonResponse({'message' : 'Already exists phone_number'}, status = 400)

            if User.objects.filter(username = username).exists():
                return JsonResponse({'message' : 'Already exists username'}, status = 400)

            if User.objects.filter(email = email).exists():
                return JsonResponse({'message' : 'Already exists email'}, status = 400)

            User.objects.create(
                name         = name,
                phone_number = phone_number,
                email        = email,
                username     = username,
                password     = password
                )
            return JsonResponse({'message' : 'All done!'}, status = 201)
        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status = 400)

class SigninView(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            username     = data['username']
            phone_number = data['phone_number']
            email        = data['email']
            password     = data['password']

            if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists() or User.objects.filter(phone_number=phone_number).exists():    
                if password =='':
                    return JsonResponse({'message': 'Check your Input'},status = 401)

                if User.objects.filter(password=password).exists():
                    return JsonResponse({'message': 'All done!'}, status = 200)

                else:
                    return JsonResponse({'message': 'Check your password'}, status = 401)

            else:
                return JsonResponse({'message': 'Check your ID'}, status = 401)

        except KeyError:
            return JsonResponse({'message': 'KEY ERROR'},status = 400)