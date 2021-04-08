import json,traceback
import bcrypt
import jwt

from django.http                import JsonResponse
from django.core.exceptions     import ValidationError
from django.views               import View
from django.db.models           import Q

from users.models               import User
from .validations               import validate_email, validate_phone, validate_password
from my_settings                import SECRET_KEY

class SignUpView(View):
    def post(self,request):

        try:
            data = json.loads(request.body)

            if not data['email'] or not data['password']:
                return JsonResponse({'message': 'NO_VALUES_'}, status=400)

            if not validate_email(data['email']):
                return JsonResponse({'message': 'USE_VALID_EMAIL'}, status=401)

            if not validate_password(data['password']):
                return JsonResponse({'message': 'PASSWORD_TOO_SHORT'}, status=402)

            hashed_password = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt()).decode()

            User.objects.create(
                email        = data['email'],
                password     = hashed_password,
                phone_number = data.get('phone_number',None),
                name         = data.get('name',None),
                nickname     = data.get('nickname',None)
            )
            return JsonResponse({'message': 'SUCCESS',"user_email":data['email']}, status=201)

        except ValidationError as VE:
            trace_back = traceback.format_exc()

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


class LogInView(View):
    def post(self,request):
        data = json.loads(request.body)

        try:

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'ID_NOT_EXIST'}, status=401)

            user_email = User.objects.get(email=data['email'])
            if not bcrypt.checkpw(data['password'].encode('utf-8'), user_email.password.encode('utf-8')):
                return JsonResponse({'message': 'INCORRECT_PASSWORD'}, status=402)

            access_token = jwt.encode({'id': user_email.id}, 'secret', algorithm='HS256')
            return JsonResponse({'token': access_token,'message':'SUCCESS','user_email':data['email']},status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)




