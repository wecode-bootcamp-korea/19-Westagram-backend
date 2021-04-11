import jwt
import json
import requests

from django.http            import JsonResponse

from accounts.models        import User

def login_check(func):
    def wrapper(self,request,*args, **kwargs):
    #     try:
    #         access_token = request.headers.get(‘Authorization’, None)
    #         unhashed = jwt.decode(access_token, 'secret', algorithm=‘HS256’)
    #         if User.objects.filter(id=unhashed[‘id’]).exists():
    #             login_user = User.objects.filter(id=unhashed[‘id’])
    #             return func(self, request, *args, **kwargs)
    #         else:
    #         return JsonResponse({‘message’:“UNAUTHORIZED_USER”}, status=400)

    #     except jwt.exceptions.DecodeError:
    #         return JsonResponse({‘message’ : ‘INVALID_TOKEN’}, status=400)
    #     except KeyError:
    #         return JsonResponse({‘message’ : ‘No_TOKEN’ }, status=400)
    # return wrapper

        try:
            access_token = request.headers.get('Authorization', None)          
        #    print('--'*30)
        #    print(access_token)
            payload = jwt.decode(access_token, 'secret', algorithms='HS256')        # 디코드 할 때는 algorithms 사용, 인코딩 할 때는 algorithm 사용
        #    print('*'*30)
            user = User.objects.get(id=payload['user_id'])                 
            request.user = user                                     

        except jwt.exceptions.DecodeError:                                     
            return JsonResponse({'message' : 'INVALID_TOKEN' }, status=400)

        except User.DoesNotExist:                                           
            return JsonResponse({'message' : 'INVALID_USER'}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper