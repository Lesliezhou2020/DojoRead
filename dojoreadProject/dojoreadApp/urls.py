from django.urls import path
from .import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('books', views.books),
    path('logout', views.logout),
    path('books/add', views.newbook),
    path('books/<int:book_id>',views.book_detail),
    path('users/<int:user_id>', views.user_detail),
    path('review/<int:review_id>/deletet',views.delete),
    path('review/add', views.add_review),
    
   
    
]
