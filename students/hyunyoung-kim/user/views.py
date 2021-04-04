import json

from django.http       import JsonResponse
from django.views      import View

from .models           import User
from .my_exceptions    import *
from .utils            import email_check
from .utils            import password_check
from .utils            import duplicate_email_check
from .utils            import duplicate_nickname_check


class Signup(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            email      = data['email']
            name       = data['name']
            nickname   = data['nickname']
            password   = data['password']

            if not(email_check(email)):
                raise InvalidEmail('INVALID_EMAIL_ADDRESS')
            
            if not(password_check(password)):
                raise InvalidPassword('INVALID_PASSWORD')

            if duplicate_email_check(email):
                raise AlreadyExistEmail('ALREADY_EXISTS_EMAIL')

            if duplicate_nickname_check(nickname):
                raise AlreadyExistNickname('ALREADY_EXISTS_NICKNAME')

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        except InvalidEmail as e:
            return JsonResponse({'MESSAGE':f'{e}'}, status=400)
        
        except InvalidPassword as e:
            return JsonResponse({'MESSAGE':f'{e}'}, status=400)

        except AlreadyExistEmail as e:
            return JsonResponse({'MESSAGE':f'{e}'}, status=400)

        except AlreadyExistNickname as e:
            return JsonResponse({'MESSAGE':f'{e}'}, status=400)

        except Exception as e:
            print('Error occured', e)
            return JsonResponse({'MESSAGE':'SERVER_ERROR'}, status=500)  

        else:
            User.objects.create(
                email    = email,
                name     = name,
                nickname = nickname, 
                password = password
                )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)



    
 
        
            


