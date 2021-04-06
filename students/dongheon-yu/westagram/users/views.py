import bcrypt
import jwt
import json

from django.http  import JsonResponse
from django.views import View 
from .models      import User 

class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        email       = data['email']
        name        = data['name']
        phoneNumber = data['phoneNumber']
        password    = data['password']
        
        if not (email or password):
            return JsonResponse({"message" : "KEY_ERROR."}, status = 400)
        
        try:
            if User.objects.filter(email = data['email']).exists() == True:
                return JsonResponse({"message" : "같은 아이디가 존재합니다."}, status = 401)
        except:
            pass

        if ('@' or '.') not in email:
            return JsonResponse({"message" : "아이디를 제대로 써주세요"}, status = 401)

        if len(password) < 6:
            return JsonResponse({"message" : "비밀번호를 5글자 이상으로 늘려주세요"}, status = 401)

        else:
            User.objects.create(
                    email       = data['email'],
                    name        = data['name'],
                    phoneNumber = data['phoneNumber'],
                    password    = data['password']
            )
            return JsonResponse({"message" : "Success"}, status = 200)
        

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        email = data['email'] 
        password = data['password']
        
        try:
            if User.objects.filter(email=email).exists():
                if User.objects.get(email=email).password == password:
                    return JsonResponse({"message": "SUCCESS"}, status=200)
                else:
                    return JsonResponse({"message": "INVALID_PASSWORD"}, status=401)
            else:
                return JsonResponse({"message": "INVALID_EMAIL"}, status=401)
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        
        
        
