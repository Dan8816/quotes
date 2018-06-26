from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from apps.first_app.models import User, UserManager, Quote
from django.contrib import messages
import re, bcrypt

def index(request):
    return render(request, 'first_temps/index.html')

def create(request):
    errors = User.objects.basic_validator(request.POST)
    if errors:
            print(errors)
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
    else:
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['confirmpassword'].encode(), bcrypt.gensalt())
        )
        print("successfully created users")
        request.session['user_id']=new_user.id
        request.session['first_name']=request.POST['first_name']
        request.session['last_name']=request.POST['last_name']
        request.session['email']=request.POST['email']
        return redirect('/success')##this will need to direct to the users quotes wall

def login(request):
    if User.objects.filter(email=request.POST['email']):
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            print('email and password matches, successful login')
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['user_id'] = user.id
            request.session['email'] = user.email
            return redirect('/success')##this will go to the users quote wall
        else:
            print("failed password")
            return redirect('/')

def logout(request):
    request.session.clear()    
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "quotes" : Quote.objects.order_by("like_count")[:12],
        "users" : User.objects.all(),
    }
    print(request.session['user_id'])
    return render(request, "first_temps/success.html", context)##this renders quote wall

def create_quote(request):
    errors = Quote.objects.quote_validator(request.POST)
    if errors:
            print(errors)
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/success')
    else:
        Quote.objects.create(author=request.POST['author'], quote=request.POST["quote"], user_id=request.session['user_id'])
        return redirect('/success')

def del_quote(request, id):
    d = Quote.objects.get(id=id)
    if int(request.session['user_id']) == d.user_id:
        d.delete()
        return redirect('/success')
    else:
        print("You did not post this")
        return redirect('/success')


def myaccount(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            "user" : User.objects.filter(id=user_id)
        }
    return render(request, "first_temps/myaccount.html")

def update(request):
    errors = User.objects.update_validator(request.POST)
    if errors:
            print(errors)
            for key, value in errors.items():
                messages.error(request, value)
            return render(request, "first_temps/myaccount.html", errors)
    else:
        this_user = User.objects.get(id=request.session['user_id'])
        this_user.first_name = request.POST['first_name']
        this_user.last_name = request.POST['last_name']
        this_user.email = request.POST['email']
        this_user.save()
        print("successfully updated user")
        request.session['first_name']=request.POST['first_name']
        request.session['last_name']=request.POST['last_name']
        request.session['email']=request.POST['email']
        return redirect('/success')


def thisUserQuotes(request, user_id):
    context = {
        "user" : User.objects.filter(id=user_id),
        "quotes" : Quote.objects.filter(user_id=user_id)
    }
    print(context)
    return render(request, "first_temps/this_user.html", context)

def like(request, id):
    this_user = User.objects.get(id=request.POST['user_id'])
    this_quote = Quote.objects.get(id=id)
    this_quote.likes.add(this_user)
    this_quote.like_count += 1
    this_quote.save()
    return redirect('/success')