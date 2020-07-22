from django.shortcuts import render,redirect
from .models import Profile,User,Following,Post
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib import messages
from .forms import UserForm,ProfileForm,PostForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q

@login_required(login_url='login')
def IndexView(request):
    profile = False
    # print("------",request.user,request.user.profile)
    try:
        profile = request.user.profile
    except:
        pass
    profiles = Profile.objects.exclude(id=profile and profile.id)
    return render(request,'index.html',{'profile':profile,'explore_profiles':profiles})

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
        profileform = ProfileForm(request.POST,request.FILES)
        if profile:
            profileform = ProfileForm(request.POST,request.FILES,instance=profile)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            messages.success(request,"Profile is Updated Successfully")
            return redirect('index')
        else:
            messages.error(request,"There is a problem in updating profile. Please try later.")
    userform = UserForm(instance=request.user)
    profileform = ProfileForm()
    if profile:
        profileform = ProfileForm(instance=profile)
    context= {'userform':userform,'profileform':profileform}
    print(context)
    return render(request,'updateprofile.html',context=context)

@login_required(login_url='login')
def createPostView(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user= request.user
            post.save()
            return redirect('index')
    form = PostForm()
    return render(request,'post.html',{'form':form})

def follower_check_api_view(request,target,follower):
    following = Profile.objects.filter(
        Q(followers__target_id=target) & 
        Q(followers__follower_id=follower)
        ).exists()
    dict = {'following':following}
    return JsonResponse(dict)

def follow_api_view(request,target,follower):
    profile = request.user.profile
    following = Following.objects.create(target_id=target,follower_id=follower)
    profile.followers.add(following)
    print(profile.followers)
    dict = {'is_followed':True}
    return JsonResponse(dict)

def unfollow_api_view(request,target,follower):
    print("=======")
    profile = request.user.profile
    following = Following.objects.filter(target_id=target,follower_id=follower)
    profile.followers.remove(following)
    following.delete()
    dict = {'is_unfollowed':True}
    return JsonResponse(dict)

    
    
    