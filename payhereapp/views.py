# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json, re, bcrypt, jwt

from django.views          import View
from django.http           import JsonResponse

from django.core.paginator  import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

from  my_settings           import SECRET_KEY
from .models                import User, Book
from core.decorators        import login_decorator

class SignUp(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)
            email           = data['email']
            password        = data['password']
            hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())

            if User.objects.filter(email=email).exists():
                return JsonResponse({"MESSAGE": "EMAIL_ALREADY_EXIST"}, status=400)

            if not re.match(r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
                return JsonResponse({"MESSAGE": "INVALID_FORMAT"}, status=400)

            if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$", password):
                return JsonResponse({"MESSAGE": "INVALID_FORMAT"}, status=400)

            User.objects.create(
                nickname =   data.get('nickname'), #선택적으로 입력받을 때
                email    =   email,
                password =   hashed_password.decode('UTF-8'),
            )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

class SignIn(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)      
            email    = data['email']
            password = data['password']        

            if not User.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE':'EMAIL_NOT_EXIST'}, status = 401)

            if bcrypt.checkpw(password.encode('utf-8'),User.objects.get(email=email).password.encode('utf-8')):
                token = jwt.encode({'id':User.objects.get(email=email).id}, SECRET_KEY)
            
                return JsonResponse({'TOKEN': token}, status = 200)

            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

class Book(View):
    @login_decorator
    def post(self, request):
        try:
            data   = json.loads(request.body)

            Book.objects.create(
                user_id = request.user.id,
                change  = data['change'],
                memo    = data.get('memo')
            )

            return JsonResponse({'MESSAGE': 'SUCCEESS'}, status = 200)
            
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

class BookList(View):
    def get(self, request):
        try:
            books = Book.objects.filter(user_id=request.user.id, is_deleted=False)

            result = [{
                "change"     : book.change,
                "memo"       : book.memo,
                "created_at" : book.created_at
            } for book in books]

            return JsonResponse({'RESULT': result}, status = 200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

