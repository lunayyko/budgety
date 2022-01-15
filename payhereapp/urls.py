from django.urls import path
from .views      import SignUp, SignIn, BookList, Book

urlpatterns = [
    path("book", BookList.as_view()),
    path("book/<int:post_id>", Book.as_view()),
    path("signup", SignUp.as_view()),
    path("signin", SignIn.as_view()),
]