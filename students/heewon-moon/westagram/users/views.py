import json
import bcrypt
import jwt

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q

from .models            import User
from .validators        import email_validator, password_validator, phone_validator
from westagram.settings import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']
            nickname = data['nickname']
            phone    = data['phone']

            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE' : 'EMAIL ALREADY EXISTS'}, status=400)

            if not email_validator(email):
                return JsonResponse({'MESSAGE' : 'INVALID EMAIL'}, status=400) 

            if not password_validator(password):
                return JsonResponse({'MESSAGE' : 'INVALID PASSWORD'}, status=400)

            if not phone_validator(phone):
                return JsonResponse({'MESSAGE' : 'INVALID PHONE NUMBER'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

            User.objects.create(
                email    = email,
                password = hashed_password,
                nickname = nickname,
                phone    = phone
            )

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            account  = data['account']
            password = data['password']
            
            user = User.objects.filter(Q(email=account) | Q(phone=account) | Q(nickname=account))

            if not user:
                return JsonResponse({'MESSAGE' : 'INVALID USER'}, status=401)
            user = user[0]
            
            input_password = password.encode('utf-8')
            db_password = user.password.encode('utf-8')

            if bcrypt.checkpw(input_password, db_password):
                token = jwt.encode({'user_id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)
                return JsonResponse({'MESSAGE' : 'SUCCESS', 'token' : token}, status=200)
            
            return JsonResponse({'MESSAGE' : 'WRONG PASSWORD'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)