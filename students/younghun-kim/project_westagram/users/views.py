import json

from django.http            import JsonResponse, response
from django.core.exceptions import ValidationError
from django.views           import View

from users.models import User

class RegisterView(View):
    def post(self, request):
        data = json.loads(request.body)
        useremail   = data['useremail']
        password    = data['password']
        re_password = data['re_password']

        try:
            if User.objects.get(useremail=useremail):
                response_message = "Duplicate_Useremail"
                status_code = 400
        
                return JsonResponse({"message":response_message}, status = status_code)
        except:
            pass

        if not (useremail and password and re_password):
            response_message = "KEY_ERROR"
            status_code      = 400
        
        elif not ('@' in useremail) or not ('.' in useremail ):
            raise ValidationError("Enter a valid useremail")
            
        elif len(password) < 8:
            raise ValidationError("Password mus be at least 8 characters")

        elif password != re_password:
            raise ValidationError("Password_MISMATCH")
 
        else:
            User.objects.create(
                useremail = useremail,
                password = password,
            )

            response_message = "SUCCESS"
            status_code      = 200

        return JsonResponse({"message":response_message}, status = status_code)
   
