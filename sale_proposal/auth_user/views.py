from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages


def registerView(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = request.POST.get('email')
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            user = authenticate(username=username, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            if user.is_active:
                messages.success(request, "Account Created Successfully")
                login(request, user)
                return redirect('/')
    return render(request, 'frontend/register.html', {'form': form})

def loginView(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            return redirect('/')
        else:
            messages.error(request,"Invalid Username or Password!")
    return render(request,'frontend/login.html',{'form':form})

def logoutView(request):
    logout(request)
    return redirect('login')
