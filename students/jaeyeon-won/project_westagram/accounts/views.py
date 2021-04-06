import json
import re
import bcrypt
import jwt

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

            hashed_password     = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                name         = name,
                phone_number = phone_number,
                email        = email,
                username     = username,
                password     = hashed_password
                )
            return JsonResponse({'message' : 'Success!'}, status = 201)

        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status = 400)

class SigninView(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            user     = data['user']
            password = data['password']

            if User.objects.filter(username=user).exists():
                user = User.objects.get(username=user)

            elif User.objects.filter(email=user).exists():
                user = User.objects.get(email=user)

            elif User.objects.filter(phone_number=user).exists():
                user = User.objects.get(phone_number=user)

            else:
                return JsonResponse({'message': 'Check your ID'},status = 401)
         
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({'user_id': user.id}, 'secret', algorithm='HS256')
                return JsonResponse({'token' : token, 'message': 'Success!'}, status=200)

            else:
                return JsonResponse({'message': 'Check your password'}, status = 401)

        except KeyError:
            return JsonResponse({'message': 'KEY ERROR'},status = 400)