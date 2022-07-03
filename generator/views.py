from django.shortcuts import render
from django.http import HttpResponse
import random

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

    password = ''.join(random.sample(chars, length))

    return render(request, 'generator/password.html', {'password':password})

def about(request):
    return render(request, 'generator/about.html')