import json
import bcrypt

from django.http            import JsonResponse, response
from django.views           import View

from users.models import User

class SignupView(View):
    def post(self, request):
        data         = json.loads(request.body)
        email        = data['email']
        password     = data['password']
        name         = data['name']
        phone_number = data['phone_number']

        if User.objects.filter(email=email).exists():
            return JsonResponse({"message":"Duplicate_Useremail"}, status = 400)

        if not (email and password):
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)

        if not ('@' in email) or not ('.' in email ):
            return JsonResponse({"message":"Enter a valid useremail"}, status = 400)

        if len(password) < 8:
            return JsonResponse({"message":"Password must be at least 8 characters"}, status = 400)
        
        else:
            hashed_password  = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
            User.objects.create(
                email        = email,
                password     = hashed_password,
                name         = name,
                phone_number = phone_number,
            )

            return JsonResponse({"message":"SUCCESS"}, status = 200)
   
