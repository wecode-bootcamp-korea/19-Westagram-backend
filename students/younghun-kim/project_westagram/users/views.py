
import bcrypt
import json
import jwt
import my_settings 

from django.http            import JsonResponse, response
from django.views           import View

from .models import User

class SignupView(View):
    def post(self, request):
        data            = json.loads(request.body)
        PASSWORD_LENGTH = 8

        try:
            email        = data['email']
            password     = data['password']
            name         = data['name']
            phone_number = data['phone_number']

            if name == '' or phone_number == '':
                return JsonResponse({'message' : "Empty name or phone_number"}, status =400)

            if not ('@' in email) or not ('.' in email ):
                return JsonResponse({"message":"Enter a valid useremail"}, status = 400)
            
            if len(password) < PASSWORD_LENGTH:
                return JsonResponse({"message":"At least 8 characters"}, status = 400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message":"Duplicate_Useremail"}, status = 400)

            hashed_password  = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode()
            User.objects.create(
                email        = email,
                password     = hashed_password,
                name         = name,
                phone_number = phone_number,
            )
        
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
        
        return JsonResponse({"message":"SUCCESS"}, status = 200)
   
class  LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            email         = data['email']
            password      = data['password']
            name          = data.get('name')
            phone_number  = data.get('phone_number')

            user          = User.objects.filter(email=email)

            if not user.exists():
               return JsonResponse({"message":"INVALID_USER"}, status = 401)
 
            user_password = user.first().password 

            if not bcrypt.checkpw(password.encode('utf-8'), user_password.encode('UTF-8')):
                return JsonResponse({"message":"INVALID_USER"}, status = 401)
                
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)

        access_token = jwt.encode({'id' : user.first().id}, my_settings.SECRET['secret'], algorithm='HS256')

        return JsonResponse({"message":"SUCCESS",'token' : access_token, 'user_email' : user.first().email},  status = 200)
