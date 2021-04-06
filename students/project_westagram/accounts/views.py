import json
from json import decoder
import bcrypt
import jwt
import re

from django.http    import JsonResponse
from django.views   import View

from .models        import Accounts

# 회원가입 뷰
class SignupView(View):

    def post(self, request):
        data     = json.loads(request.body)
        accounts = Accounts.objects.all()
        
        email_validation    = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        password_validation = re.compile('[(<`~!@#$%^&*,./?;:>)_]+')
        name_validation     = re.compile('[ㄱ-ㅎㅏ-ㅣ]+')
        phone_validation    = re.compile('[0-9]+')
        
        max_password = 30
        min_password = 8
        max_phone    = 11
        min_phone    = 10
        
        try:
            if accounts.filter(email = data['email']).exists():
                return JsonResponse({'message': f"E-mail({data['email']}) already exist"}, status = 400)
            if not email_validation.match(data['email']):
                return JsonResponse({'message': f"{data['email']} is Invalid E-mail"}, status = 400)

            if len(data['password']) < min_password or len(data['password']) > max_password:
                return JsonResponse({'message': 'Password too short!'}, status = 400)
            if not re.search('[a-zA-Z]+', data['password']) or not re.search('[0-9]+', data['password']):
                return JsonResponse({'message': 'Invalid Password(각 하나 이상의 소문자 또는 대문자 그리고 숫자를 포함하세요)'}, status = 400)
            if not password_validation.search(data['password']):
                return JsonResponse({'message': 'Invalid Password(하나 이상의 특수문자를 포함하세요)'}, status = 400)
            encrypted_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            if name_validation.search(data['name']):
                return JsonResponse({'message': f"{data['name']} is Invalid Name"}, status = 400)
            
            if len(data['phone']) > max_phone or len(data['phone']) < min_phone or not phone_validation.match(data['phone']):
                return JsonResponse({'message': f"{data['phone']} is Wrong PHONE number"}, status = 400)
            if accounts.filter(phone = data['phone']).exists():
                return JsonResponse({'message': f"PHONE number({data['phone']}) already exist"}, status = 400)

            
            
            Accounts.objects.create(email    = data['email'],
                                    password = encrypted_password,
                                    name     = data['name'],
                                    phone    = data['phone'],
                                    )
                
            return JsonResponse({"message": "Sign up complete!"}, status = 201)
        
        except KeyError as error_source:
            return JsonResponse({'message': f"KEY ERROR! '{error_source}' is incorrect"}, status = 400)

# 로그인 뷰
class LoginView(View):
    
    def post(self, request):
        data = json.loads(request.body)
        
        email_validation = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        phone_validation = re.compile('[0-9]')
        
        try:
            if request_email := data.get('email'):
                if not email_validation.match(request_email):
                    return JsonResponse({'message': f'Invalid USER, {request_email} is not email form'}, status = 401)
                if Accounts.objects.filter(email = request_email).exists():
                    if Accounts.objects.get(email = request_email).password == data['password']:
                        return JsonResponse({'message': 'Log in SUCCESS'}, status = 200)
                    else:
                        return JsonResponse({'message': 'Wrong PASSWORD'}, status = 200)
                else:
                    return JsonResponse({'message': f'Invalid USER, {request_email} doesn\'t exist'}, status = 401)
                
            if request_name := data.get('name'):
                if Accounts.objects.filter(name = request_name).exists():
                    if data["password"] == Accounts.objects.get(name = request_name).password:
                        return JsonResponse({'message': 'Log in SUCCESS'}, status = 200)
                    else:
                        return JsonResponse({'message': 'Wrong PASSWORD'}, status = 200)
                else:
                    return JsonResponse({'message': f'Invalid USER, {request_name} doesn\'t exist'}, status = 401)
                
            if request_phone := data.get('phone'):
                if not phone_validation.match(request_phone):
                    return JsonResponse({'message': f'Invalid USER, Your phone \'{request_phone}\' is worng number'}, status = 401)
                if Accounts.objects.filter(phone = request_phone).exists():
                    if Accounts.objects.get(phone = request_phone).password == data['password']:
                        return JsonResponse({'message': 'Log in SUCCESS'}, status = 200)
                    else:
                        return JsonResponse({'message': 'Wrong PASSWORD'}, status = 200)
                else:
                    return JsonResponse({'message': f'Invalid USER, Your phone \'{request_phone}\' doesn\'t exist'}, status = 401)
                
        except KeyError as error_source:
            return JsonResponse({'message': f"KEY ERROR, {error_source} is WRONG"}, status = 400)
        
        except Accounts.DoesNotExist as error_source:
            return JsonResponse({'message': f"{data['']} is Invalid ID"}, status = 400)
    pass