# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json, re, bcrypt, jwt, datetime

from django.views          import View
from django.http           import JsonResponse

from django.db.models       import Sum
from django.core.exceptions import ObjectDoesNotExist

from  my_settings           import SECRET_KEY, ALGORITHM
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
            
            user = User.objects.get(email=email)

            if bcrypt.checkpw(password.encode('utf-8'),user.password.encode('utf-8')):
                token = jwt.encode({'user_id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
                
                return JsonResponse({'TOKEN': token}, status = 200)

            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

class BookView(View):
    @login_decorator
    def post(self, request):
        try:
            data   = json.loads(request.body)

            Book.objects.create(
                memo    = data.get('memo'),
                user_id = request.user.id,
                amount  = data['amount']
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status = 200)
            
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)
    
    @login_decorator
    def get(self, request):
        try:
            books = Book.objects.filter(user_id = request.user.id, is_deleted=False)

            results = [{
                "book_id"    : book.id,
                "created_at" : book.created_at.date(),
                "updated_at" : book.updated_at.date(),
                "amount"     : book.amount,
                "memo"       : book.memo
            } for book in books]

            total = Book.objects.all().aggregate(Sum('amount'))
            
            return JsonResponse({'results': results, 'total' : total }, status = 200)
            
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)
        except ObjectDoesNotExist:
            return JsonResponse({'MESSAGE':'NOT_EXIST'}, status = 400)

class BookLog(View):
    @login_decorator
    def get(self, request):
        try:
            books = Book.objects.filter(user_id=request.user.id)

            results = [{
                "created_at" : book.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at" : book.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                "id"         : book.id,
                "amount"     : book.amount,
                "memo"       : book.memo,
                "is_deleted" : book.is_deleted,
                "deleted_at" : book.deleted_at.strftime("%Y-%m-%d %H:%M:%S") if book.deleted_at is not None else None
            } for book in books]

            return JsonResponse({'results': results}, status = 200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

class BookModify(View):
    @login_decorator
    def get(self, request, book_id):
        try:
            book = Book.objects.get(user_id=request.user.id, id = book_id)

            result = {
                "created_at" : book.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at" : book.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                "amount"     : book.amount,
                "memo"       : book.memo,
                "is_deleted" : "no" if book.is_deleted is False else "yes",
                "deleted_at" : book.deleted_at.strftime("%Y-%m-%d %H:%M:%S") if book.deleted_at is not None else None
            }
            return JsonResponse({'result': result}, status = 200)
            
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)
        except ObjectDoesNotExist:
            return JsonResponse({'MESSAGE':'NOT_EXIST'}, status = 400)

    @login_decorator
    def patch(self, request, book_id):
        try:
            data   = json.loads(request.body)
            book = Book.objects.filter(user_id=request.user.id, id = book_id)
            
            book.update(
                memo    = data.get('memo'),
                amount  = data['amount']
            )

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)
    
    @login_decorator
    def delete(self, request, book_id):
        try:
            book = Book.objects.get(user_id=request.user.id, id = book_id)
            book.is_deleted = True
            book.deleted_at = datetime.datetime.now()
            book.save()

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)
