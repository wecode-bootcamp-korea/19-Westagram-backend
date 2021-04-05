import json
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
        password_validation = re.compile('[(<`~!@#$%^&*,./?;:>)]+')
        phone_validation    = re.compile('[0-9]')
        
        max_password = Accounts.max_password
        min_password = Accounts.min_password
        max_phone    = Accounts.max_phone
        min_phone    = Accounts.min_phone
        
        try:
            if Accounts.objects.filter(email = data['email']).exists():
                return JsonResponse({'message': 'KEY_ERROR E-mail already exist'}, status = 400)
            if not email_validation.match(data['email']):
                return JsonResponse({'message': 'KEY_ERROR Invalid E-mail'}, status = 400)

            if len(data['password']) < min_password or len(data['password']) > max_password:
                return JsonResponse({'message': 'KEY_ERROR Password too short!'}, status = 400)
            if not re.findall('[a-zA-Z]+', data['password']) or not re.findall('[0-9]+', data['password']):
                return JsonResponse({'message': 'KEY_ERROR Invalid Password(각 하나 이상의 소문자, 대문자, 숫자를 포함하세요)'}, status = 400)
            if not password_validation.findall(data['password']):
                return JsonResponse({'message': 'KEY_ERROR Invalid Password(하나 이상의 특수문자를 포함하세요)'}, status = 400)
            
            if (len(data['phone']) > max_phone or len(data['phone']) < min_phone) and not phone_validation.match(data['phone']):
                return JsonResponse({'message': 'KEY_ERROR Wrong PHONE number'}, status = 400)
            if Accounts.objects.filter(phone = data['phone']).exists():
                return JsonResponse({'message': 'KEY_ERROR PHONE number already exist'}, status = 400)

            Accounts.objects.create(email    = data['email'],
                                    password = data['password'],
                                    name     = data['name'],
                                    phone    = data['phone'],
                                    )
                
            return JsonResponse({"message": "Sign up complete!"}, status = 201)
        except KeyError as ke:
            return JsonResponse({'message': f'KeyError! {ke} is incorrect'}, status = 400)

# 로그인 뷰
class LoginView(View):
    pass
#     def post(self, request):
#         data = json.loads(request.body)
        
#         email_validation = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
#         phone_validation = re.compile('[0-9]')
        
#         try:
#             if not email_validation.match(data['email']):
#                 return JsonResponse({'message': 'Invalid USER, ID should be email or phone number'}, status = 401)
        
#             if not Accounts.objects.filter(email = data['email']).exists():
#                 return JsonResponse({'message': 'Invalid USER, E-mail doesn\'t exist'}, status = 401)
#             elif data['user_pw'] == Accounts.objects.get(email = data['email']).user_pw:
#                 return JsonResponse({'message': 'Log in SUCCESS'}, status = 200)
#             else:
#                 return JsonResponse({'message': 'Wrong Password'}, status = 401)
        
#         except SyntaxError:
#             if not phone_validation.match(data['user_phone']):
#                 return JsonResponse({'message': 'Invalid USER, ID should be email or phone number'}, status = 401)
            
#             if not Accounts.objects.filter(user_phone = data['user_phone']).exists():
#                 return JsonResponse({'message': 'Invalid USER, ID doesn\' exist'}, status = 401)
#             elif data['user_pw'] == Accounts.objects.get(user_phone = data['user_phone']).user_pw:
#                 return JsonResponse({'message': 'Log in SUCCESS'}, status = 200)
#             else:
#                 return JsonResponse({'message': 'Wrong Password'}, status = 401)
            
#         except:
#             return JsonResponse({'message': 'KEY ERROR'}, status = 400)