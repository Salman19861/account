from email import message
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import *
from django.contrib.auth.forms import AuthenticationForm,SetPasswordForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.contrib.auth.models import User

# Create your views here.
def create(request):
    if request.method=='POST':
        fm=createForm(request.POST)
        if fm.is_valid():
            fm.save()
            email=fm.cleaned_data['email']
            token=str(uuid.uuid4())
            
            send_mail(
        'Click below link to verify ur account',
        f'http://127.0.0.1:8000/verify/{token}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
        )
            messages.success(request,'check ur mail to verify ur account')
            return HttpResponseRedirect('/login/')
    else:
        fm=createForm()   
    return render(request,'account/createForm.html',{'form':fm})

def loginUser(request):
    if request.method=='POST':
        fm=AuthenticationForm(request.POST,data=request.POST)
        if fm.is_valid():
            username=fm.cleaned_data['username']
            password=fm.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_superuser:
                    login(request,user)
                    return HttpResponseRedirect('/Dashboard/dashboard')
                messages.success(request,'please verify ur email')
                return HttpResponseRedirect('/login/')
    else:
        fm=AuthenticationForm()
    return render(request,'account/login.html',{'form':fm})

def verifyUser(request,token):
    user=User.objects.last()
    print(user)
    if user.is_superuser:
        messages.success(request,'already verified')
    else:
        user.is_superuser=True
        user.save()
    return HttpResponseRedirect('/login/')

def logoutUser(request):
    logout(request)
    messages.success(request,'logged out successfully')
    return HttpResponseRedirect('/login/')

def forgetPassword(request):
    if request.method=='POST':
        email=request.POST.get('email')
        check=User.objects.filter(email=email)
        if check:
            token=str(uuid.uuid4())
            send_mail(
        'Click below link to verify ur Email',
        f'http://127.0.0.1:8000/newPassword/{token}/',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
        )
            messages.success(request,'check ur mail to verify email')
            return HttpResponseRedirect('/forgetPassword/')
        else:
            messages.success(request,'user not found !')
            return HttpResponseRedirect('/forgetPassword/')
        
    return render(request,'account/forgetPassword.html')


def newPassword(request,token):
    if request.method=='POST':
        email=request.POST.get('email')
        passw=request.POST.get('passw')
        passw2=request.POST.get('passw2')

        if passw!=passw2:
            messages.success(request,"passwords doesn't match")
            return HttpResponseRedirect(f'/newPassword/{token}')

        
        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request,'re-enter email correctly')
            return HttpResponseRedirect(f'/newPassword/{token}')

        user.set_password(passw)
        user.save()
        messages.success(request,'password setted successfully')
        return HttpResponseRedirect('/login/')
    
    
    return render(request,'account/setPassword.html',{})