import json
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
                return JsonResponse({'message': "Already exist email"}, status = 400)
            if not email_validation.match(data['email']):
                return JsonResponse({'message': "Invalid email"}, status = 400)

            if len(data['password']) < min_password or len(data['password']) > max_password:
                return JsonResponse({'message': 'Password too short!'}, status = 400)
            if not re.search('[a-zA-Z]+', data['password']) or not re.search('[0-9]+', data['password']):
                return JsonResponse({'message': 'Invalid Password(각 하나 이상의 소문자 또는 대문자 그리고 숫자를 포함하세요)'}, status = 400)
            if not password_validation.search(data['password']):
                return JsonResponse({'message': 'Invalid Password(하나 이상의 특수문자를 포함하세요)'}, status = 400)
            encrypted_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            if name_validation.search(data['name']):
                return JsonResponse({'message': "Invalid Name"}, status = 400)
            
            if accounts.filter(nickname = data['nickname']).exists():
                return JsonResponse({'message': 'Already exist nickname'}, status = 400)
            
            if len(data['phone']) > max_phone or len(data['phone']) < min_phone or not phone_validation.match(data['phone']):
                return JsonResponse({'message': "Invalid phone number"}, status = 400)
            if accounts.filter(phone = data['phone']).exists():
                return JsonResponse({'message': "Already exist phone"}, status = 400)
            
            Accounts.objects.create(email    = data['email'],
                                    password = encrypted_password,
                                    name     = data['name'],
                                    nickname = data['nickname'],
                                    phone    = data['phone'],
                                    )
            
            return JsonResponse({"message": "Sign up complete!"}, status = 201)
        
        except KeyError as error_source:
            return JsonResponse({'message': f"KEY ERROR! '{error_source}' is incorrect"}, status = 400)

# 로그인 뷰
class LoginView(View):
    
    def post(self, request):
        data = json.loads(request.body)
        
        email_validation    = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        password_validation = re.compile('[(<`~!@#$%^&*,./?;:>)_]+')
        phone_validation    = re.compile('[0-9]+')
        
        accounts = Accounts.objects.all()
        
        try:
            if request_id := data.get('email'):
                if bcrypt.checkpw(data['password'].encode("utf-8"), accounts.get(email = request_id).password.encode('utf-8')):
                    return JsonResponse({'message': 'Log in SUCCESS'}, status = 200)
            
            if request_id := data.get('nickname'):
                if bcrypt.checkpw(data['password'].encode("utf-8"), accounts.get(nickname = request_id).password.encode('utf-8')):
                    return JsonResponse({'message': 'Log in SUCCESS'}, status = 200)
                
            if request_id := data.get('phone'):
                if bcrypt.checkpw(data['password'].encode("utf-8"), accounts.get(phone = request_id).password.encode('utf-8')):
                    return JsonResponse({'message': 'Log in SUCCESS'}, status = 200)
            
            # if accounts.filter(email = data["account"]).exists():
            #     request_id = accounts.get(email = data.get('account'))
            # if accounts.filter(nickname = data['account']).exists():
            #     request_id = accounts.get(nickname = data.get('account'))
            # if accounts.filter(phone = data['account']).exists():
            #     request_id = accounts.get(phone = data.get('account'))
                
            # if bcrypt.checkpw(data['password'].encode("utf-8"), request_id.password.encode('utf-8')):
            #     return JsonResponse({'message': 'Log in SUCCESS'}, status = 200)
            
        except KeyError as error_source:
            return JsonResponse({'message': f"KEY ERROR, {error_source} is WRONG"}, status = 400)
        
        except Accounts.DoesNotExist as error_source:
            return JsonResponse({'message': f"{error_source} is Invalid ID"}, status = 400)