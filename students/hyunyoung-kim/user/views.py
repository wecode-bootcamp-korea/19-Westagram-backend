import json
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View

from .models      import User
from .utils       import validate_email, validate_password
from my_settings  import SECRET


class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            email      = data['email']
            name       = data['name']
            nickname   = data['nickname']
            password   = data['password']

            if not validate_email(email):
                return JsonResponse({'MESSAGE':'INVALID_EMAIL_ADDRESS'}, status=400)
            
            if not validate_password(password):
                return JsonResponse({'MESSAGE':'INVALID_PASSWORD'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE':'ALREADY_EXISTS_EMAIL'}, status=400)

            if User.objects.filter(nickname=nickname).exists():
                return JsonResponse({'MESSAGE':'ALREADY_EXISTS_NICKNAME'}, status=400)
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                email    = email,
                name     = name,
                nickname = nickname, 
                password = hashed_password
                )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

class SingIn(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            email     = data['email']
            password  = data['password']

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE':'INVALID_USER'}, status=404)
            
            valid_password = User.objects.get(email=email).password.encode('utf-8')         

            if not bcrypt.checkpw(password.encode('utf-8'), valid_password):
                return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

            access_token = jwt.encode({'email':email}, SECRET['secret'], algorithm = 'HS256')

            return JsonResponse({'MESSAGE':'SUCCESS', 'ACCESS_TOKEN':access_token}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
