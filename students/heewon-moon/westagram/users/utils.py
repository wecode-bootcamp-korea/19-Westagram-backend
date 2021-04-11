import json
import bcrypt
import jwt

from django.http        import JsonResponse

from westagram.settings import SECRET_KEY, ALGORITHM
from users.models       import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)

            if not access_token:
                return JsonResponse({'MESSAGE' : 'UNAUTHORIZED ACCESS'}, status=401)

            payload      = jwt.decode(access_token, SECRET_KEY, ALGORITHM)

            if not User.objects.filter(id=payload['user_id']).exists():
                return JsonResponse({'MESSAGE' : 'INVALID USER'}, status=404)

            user         = User.objects.get(pk = payload['user_id'])
            request.user = user

            return func(self, request, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({'MESSAGE' : 'INVALID TOKEN'}, status=400)

    return wrapper