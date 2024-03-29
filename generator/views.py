from django.shortcuts import render, redirect, get_object_or_404
import random
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import NewPasswordForm
from .models import Passw
from django.contrib import messages
from Crypto.Cipher import AES
import hashlib

def home(request):
    return render(request, 'generator/home.html')

def password(request):
    digits = '0123456789'
    lowercase_letters = 'abcdefghijklmnopqrstuvwxyz'
    uppercase_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    punctuation = '!#$%&*+-=?@^_'
    chars = ''
    length = int(request.GET.get('length', 11))
    if request.GET.get('lowercase'):
        chars += lowercase_letters
    if request.GET.get('uppercase'):
        chars += uppercase_letters
    if request.GET.get('numbers'):
        chars += digits
    if request.GET.get('symbols'):
        chars += punctuation
    if chars == '':
        chars += lowercase_letters

    password = ''.join(random.choices(chars, k=length))
    messages.success(request, password)
    return render(request, 'generator/password.html', {'password':password})


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'generator/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'generator/signupuser.html', {'form':UserCreationForm(), 'error': 'This username has already been taken. Please, choose another one'})
        else:
            return render(request, 'generator/signupuser.html', {'form':UserCreationForm(), 'error': 'Password did not match. Please, try again'})


def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'generator/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if not user:
            return render(request, 'generator/loginuser.html', {'form':AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('home')


def createpassw(request):
    if request.method == 'GET':
        try:

            form = NewPasswordForm()
            return render(request, 'generator/createpassw.html', {'form':form})
        except:
            return render(request, 'generator/createpassw.html', {'form':NewPasswordForm(), 'error': 'Oops, something went wrong'})
    else:
        try:
            stored_messages = messages.get_messages(request)
            for message in stored_messages:
                password = message

            form = NewPasswordForm(request.POST)
            new_form = form.save(commit=False)
            
            key = hashlib.sha256(str(request.user).encode()).digest()

            cipher = AES.new(key, AES.MODE_EAX)
            new_form.passw, tag = cipher.encrypt_and_digest(str(password).encode())
            new_form.tag = tag
            new_form.nonce = cipher.nonce
            new_form.user = request.user
            new_form.save()
            
            return redirect('userpage')
        except ValueError:
            return render(request, 'generator/createpassw.html', {'form':NewPasswordForm(), 'error': 'Oops, try again'})


def userpage(request):
    notes = Passw.objects.filter(user=request.user).order_by('date')
    print(request.user)

    if 'sort_by' in request.GET:
        sort_by = request.GET['sort_by']
        if sort_by == 'title':
            notes = notes.order_by('title')
    for note in notes:

        key = hashlib.sha256(str(request.user).encode()).digest()
        decipher = AES.new(key, AES.MODE_EAX, nonce=note.nonce)
        note.passw = decipher.decrypt(note.passw)
        note.passw = note.passw.decode()
        
    return render(request, 'generator/userpage.html', {'notes': notes})


def deletepassw(request, passw_pk):
    passw = get_object_or_404(Passw, pk=passw_pk ,user=request.user)
    if request.method == 'POST':
        passw.delete()
        return redirect('userpage')
