from django.urls import path
from .views      import SignUp, SignIn, BookView, BookLog, BookModify

urlpatterns = [
    path("book", BookView.as_view()), #가계부 작성 및 리스트 확인
    path("booklog", BookLog.as_view()), #전체 로그 확인(삭제한 내역 포함)
    path("book/<int:book_id>", BookModify.as_view()), #수정, 삭제, 복구 
    path("signup", SignUp.as_view()),
    path("signin", SignIn.as_view()),
]