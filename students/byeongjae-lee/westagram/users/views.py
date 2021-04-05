import bcrypt
import json
import re

from django.views import View
from django.http  import JsonResponse

from .models      import User

class KeyError(Exception):
    pass

class InvalidEmail(Exception):
    pass

class InvalidPhoneNumber(Exception):
    pass

class InvalidPassword(Exception):
    pass

class DuplicateEmail(Exception):
    pass

class DuplicateUserId(Exception):
    pass

class DuplicatePhoneNumber(Exception):
    pass

class InvalidUser(Exception):
    pass

class SignUpView(View):

    def post(self, request):
        message     = ''
        status_code = 400
        data        = json.loads(request.body)

        
        check_email    = re.compile('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$')
        valid_email    = re.search(check_email, data['email'])
        check_password = re.compile('^(?!.*\s)(?=.*[A-Z])(?=.*\d)(?=.*[a-z])(?=.*[!@#$%&*])')
        valid_password = re.search(check_password, data['password'])
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        password = hashed_password.decode('utf-8')
        
        try:
            
            if 'email' not in data or 'password' not in data:
                raise KeyError()
            else:
                if not valid_email:
                    raise InvalidEmail()
                elif (len(data['password']) <= 8) or not valid_password:
                    raise InvalidPassword()
                elif 'phone_number' in data:
                    phone_number = str(data['phone_number'])
                    if not phone_number.isdigit() or len(phone_number) > 11 or len(phone_number) < 10 or phone_number[0] != '0':
                        raise InvalidPhoneNumber
                    elif User.objects.filter(phone_number=phone_number): 
                        raise DuplicatePhoneNumber()
                    
                    User.objects.create(
                        phone_number=phone_number,
                        password=password
                    )
                    message     = 'SUCCESS'
                    status_code = 201
                elif 'user_id' in data:
                    user_id = data['user_id']
                    if User.objects.filter(user_id=data['user_id']):
                        raise DuplicateUserId()
                    User.objects.create(
                        user_id=user_id,
                        password=password
                    )
                    message     = 'SUCCESS'
                    status_code = 201
                elif User.objects.filter(email=data['email']):
                    raise DuplicateEmail()
                elif ('email' and 'phone_number' and 'user_id') in data:
                    User.objects.create(
                            user_id      = data['user_id'],
                            email        = data['email'],
                            password     = password,
                            phone_number = phone_number 
                        )
                    message     = 'SUCCESS'
                    status_code = 201
                User.objects.create(
                    email    = data['email'],
                    password = password
                )
                message     = 'SUCCESS'
                status_code = 201
        
        except KeyError:
            
            message = 'KEY_ERROR'
            status_code = 400
        
        except InvalidEmail:
            
            message = 'INVALID_EMAIL'
            status_code = 400
        
        except InvalidPassword:
            
            message = 'INVALID_PASSWORD'
            status_code = 400
        
        except DuplicateUserId:
            
            message = 'Duplicate_User_ID'
            status_code = 400
        
        except DuplicateEmail:
            
            message = 'Duplicate_Email'
            status_code = 400
        
        except DuplicatePhoneNumber:
            
            message = 'Duplicate_Phone_Number'
            status_code = 400
        
        except InvalidPhoneNumber:
            
            message = 'INVALID_Phone_Number'
            status_code = 400


        return JsonResponse({'message': message}, status=status_code)

class LoginView(View):

    def post(self, request):

        try:

            data = json.loads(request.body)

            if (('email' or 'user_id' or 'phone_number') and 'password') not in data:
                raise KeyError()
            else:
                password = data['password']
                if 'user_id' in data:
                    
                    user_id       = data['user_id']
                    user_id_check = User.objects.filter(user_id=user_id)
                    
                    if not user_id_check:
                        raise InvalidUser
                    elif bcrypt.checkpw(password.encode('utf-8'), user_id_check.get().password.encode('utf-8')):
                        return JsonResponse({'message': 'SUCCESS'}, status=200)
                    else:
                        raise InvalidUser
                    
                elif 'email' in data:
                    
                    email       = data['email']
                    email_check = User.objects.filter(email=email)
                    
                    if not email_check:
                        raise InvalidUser
                    elif bcrypt.checkpw(password.encode('utf-8'), email_check.get().password.encode('utf-8')):
                        return JsonResponse({'message': 'SUCCESS'}, status=200)
                    else:
                        raise InvalidUser
                    
                else:
                    
                    phone_number       = str(data['phone_number'])
                    phone_number_check = User.objects.filter(phone_number=phone_number)
                    
                    if not phone_number_check:
                        raise InvalidUser
                    elif bcrypt.checkpw(password.encode('utf-8'), phone_number_check.get().password.encode('utf-8')):
                        return JsonResponse({'message': 'SUCCESS'}, status=200)
                    else:
                        raise InvalidUser
    
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except InvalidUser:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)
