from django.shortcuts import redirect, render
from django.contrib import messages
import bcrypt
from .models import *

def index(request):
    return render(request, 'index.html')


def books(request):
   
    if 'user_id' not in request.session:
        return redirect('/')
    reviews = Review.objects.all().order_by('-created_at')[:3]
    context = {
        'user': User.objects.get(id=request.session["user_id"]),
        'reviews': reviews,
        'books': Book.objects.all()
    }

    return render(request, 'books.html', context)



def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        hash_browns = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            name = request.POST['name'],
            alias = request.POST['alias'],
            email = request.POST['email'],
            password = hash_browns,
        )     
        request.session['user_id'] = user.id
        return redirect('/books')


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_to_login = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user_to_login.id 
        return redirect('/books')

def logout(request):
    request.session.flush()
    return redirect('/')


def newbook(request):
    user = User.objects.get(id=request.session['user_id'])
    if request.method =="POST":
        if request.POST['author_selection'] == '0':
            author = Author.objects.create(name=request.POST['author_name'])
        else:
            author = Author.objects.get(id=request.POST['author_selection'])
        book = Book.objects.create(
            user = user,
            title = request.POST['title'],
            author = author     
        )
        review= Review.objects.create(
            review_desc =request.POST['review'],
            rate = request.POST['rating'],
            user = user,
            book = book
        )
        
        return redirect('/books/{}'.format(book.id))
    else:
        context = {
            'user': user,
            'all_authors': Author.objects.all()        
        }
        return render(request,'add.html')


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    context={
        'book': book,
        'author': Author.objects.all(),
        'reviews':Review.objects.all(),
    }

    return render(request, 'details.html',context)

def add_review(request):
    book = Book.objects.get(id=request.POST["book_id"])
    review= Review.objects.create(
            review_desc =request.POST['reviews'],
            rate = request.POST['rating'],
            user = User.objects.get(id=request.session["user_id"]),
            book = book
        )
    return redirect('/books/{}'.format(book.id))

def user_detail(request, user_id):
    user = User.objects.get(id=user_id)
    context ={
         'user': user,
         'book': Book.objects.all,
         'reviews': Review.objects.all

    }

    return render(request, 'user.html',context)

def delete(request, review_id):
    Review.objects.get(id=review_id).delete()
    return redirect('/books/{}'.formate(book.id))







