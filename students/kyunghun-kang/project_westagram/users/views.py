import json
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View

from .models      import User
from my_settings  import SECRET_KEY

class SignUpView(View):
    def post(self, request):
        PASSWORD_LENGTH = 8
        
        try:
            data = json.loads(request.body)

            if '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'MESSGAGE': 'INVALID EMAIL'}, status=400)
            
            if User.objects.filter(email= data['email']).exists():
                return JsonResponse({'MESSGAGE': 'DUPLICATED EMAIL'}, status=400)
            
            if len(data['password']) <= PASSWORD_LENGTH:
                return JsonResponse({'MESSGAGE': 'INVALID PASSWORD'}, status=400)
            
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            User.objects.create(
                email        = data['email'],
                password     = hashed_password,
                name         = data['name'],
                phone_number = data['phone_number']
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            email       = data['email']
            password    = data['password']
            name        = data.get('name', None)
            phon_number = data.get('phon_number', None)

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE':'NOT_FOUND'}, status=404)
            
            user = User.objects.get(email=email)         
            hashed_password = user.password.encode('utf-8')
            
            if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

            access_token = jwt.encode({'user_id' : user.id}, SECRET_KEY, algorithm = 'HS256')

            return JsonResponse({'MESSAGE':'SUCCESS', 'ACCESS_TOKEN':access_token}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
