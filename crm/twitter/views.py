from django.shortcuts import render,redirect
from .models import Profile,User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib import messages
from .forms import UserForm,ProfileForm

def IndexView(request):
    return render(request,'index.html',{})

def RegisterView(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=password)
            messages.success(request,"Account Created Succesfully!")
            return redirect('login')
    return render(request,'registration.html',{'form':form})

def LoginView(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request,"Invalid Username/Password !")
    return render(request,'login.html',{'form':form})

def LogoutView(request):
    logout(request)
    return render(request,'logout.html',{})


def updateProfileView(request):
    profile = False
    profileform = False
    try:
        profile = request.user.profile
    except:
        pass
    if request.method == 'POST':
        userform = UserForm(request.POST,instance=request.user)
        if profile:
            profileform = ProfileForm(request.POST,instance=profile)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            messages.success(request,"Profile is Updated Successfully")
            return redirect('index')
        else:
            messages.error(request,"There is a problem in updating profile. Please try later.")
    userform = UserForm()
    context= {'userform':userform}
    if profile:
        context.update({'profileform':ProfileForm()})
    return render(request,'updateprofile.html',context=context)

    
    
    