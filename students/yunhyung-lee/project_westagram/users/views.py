import json
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View

from .models      import User
from project_westagram.settings  import SECRET_KEY

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            MINIMUM_PASSWORD_LENGTH = 8

            if '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'MESSAGE' : 'INVALID EMAIL'}, status=400)

            if len(data['password']) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({'MESSAGE' : 'INVALID PASSWORD'}, status=400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE' : 'DUPLICATED EMAIL'}, status=400)
        
            if User.objects.filter(phone_num=data['phone_num']).exists():
                return JsonResponse({'MESSAGE' : 'DUPLICATED PHONE_NUM'}, status=400)
            
            if User.objects.filter(name=data['name']).exists():
                return JsonResponse({'MESSAGE' : 'DUPLICATED NAME'}, status=400)

            User.objects.create(
                    name        = data['name'],
                    phone_num   = data['phone_num'],
                    password    = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                    email       = data['email']
            )
        
            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)


class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE': 'NOT FOUND'}, status=404)
           
            user = User.objects.get(email=email)
             
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                Token = jwt.encode({'User_id' : user.id}, SECRET_KEY, algorithm = 'HS256')
                return JsonResponse({'MESSAGE' : 'SUCCESS', 'Token':Token}, status=200)
        
            return JsonResponse({'MESSAGE': 'INVALID USER'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR'}, status=400)
