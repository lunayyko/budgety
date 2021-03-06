import jwt

from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from my_settings            import SECRET_KEY, ALGORITHM
from payhereapp.models      import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            pay_load     = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            user         = User.objects.get(id=pay_load['user_id'])
            request.user = user

            return func(self, request, *args, **kwargs)

        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)
        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "DECODE_ERROR"}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    return wrapper
