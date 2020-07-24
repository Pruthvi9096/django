from django.urls import reverse
from django.shortcuts import render,redirect
from .models import Profile,User,Following,Post,Comments
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib import messages
from .forms import UserForm,ProfileForm,PostForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string

@login_required(login_url='login')
def IndexView(request):
    profile = request.user.profile
    profiles = Profile.objects.select_related('user').exclude(id=profile.id)
    feed_posts = Post.objects.select_related('author').filter(
        author__followers__follower=request.user) \
        .order_by('-date_created')
    return render(request,'index.html',
        {'profile':profile,
        'explore_profiles':profiles,
        'feed_posts':feed_posts})

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
    
    profile = request.user.profile
    if request.method == 'POST':
        userform = UserForm(request.POST,instance=request.user)
        profileform = ProfileForm(request.POST,request.FILES,instance=profile)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            messages.success(request,"Profile is Updated Successfully")
            return redirect('index')
        else:
            messages.error(request,"There is a problem in updating profile. Please try later.")
    userform = UserForm(instance=request.user)
    profileform = ProfileForm(instance=profile)
    context= {'userform':userform,'profileform':profileform}
    return render(request,'updateprofile.html',context=context)

@login_required(login_url='login')
def createPostView(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author= request.user.profile
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
    user = User.objects.select_related('profile').get(id=target)
    profile = user.profile
    following = Following.objects.create(target_id=target,follower_id=follower)
    profile.followers.add(following)
    dict = {'is_followed':True}
    return JsonResponse(dict)

def unfollow_api_view(request,target,follower):
    user = User.objects.select_related('profile').get(id=target)
    profile = user.profile
    following = Following.objects.filter(target_id=target,follower_id=follower).first()
    profile.followers.remove(following)
    following.delete()
    dict = {'is_unfollowed':True}
    return JsonResponse(dict)

def profileDetailView(request,id):
    profile = Profile.objects.select_related('user').get(id=id)
    posts = profile.post_set.all()
    context = {
        'profile':profile,
        'posts':posts
    }
    return render(request,'profile.html',context=context)

def postDetailView(request,pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect(reverse('post-detail',kwargs={'pk':pk})) 
    comments = post.comments_set.filter(parent_comment__isnull=True).order_by('-date_created')
    form = CommentForm()
    return render(request,'post-detail.html',
        {'post':post,
        'comments':comments,
        'form':form})

def replyComment_api_view(request,pk):
    comment = Comments.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = comment.post
            reply.user = request.user
            reply.parent_comment = comment
            reply.save()
            return redirect(reverse('post-detail',kwargs={'pk':comment.post.pk})) 
    form = CommentForm()
    context={'commentform':form}
    form_html = render_to_string('comment_form.html',context=context,request=request)
    return JsonResponse({'form':form_html})

def deleteComment_api_view(request,pk):
    comment = Comments.objects.get(pk=pk)
    comment.delete()
    return JsonResponse({'deleted':True})

def searchView(request):
    return render(request,'search.html',{})

def search_api_view(request):
    query = request.GET.get('q')
    profiles = Profile.objects.filter(
        Q(user__username__icontains=query) |
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query)
    ).exclude(user=request.user)
    context = {
        'profiles':profiles
    }
    listItems = render_to_string('profile_list.html',context=context,request=request)
    return JsonResponse({'list':listItems})

def get_followers_list_api_view(request,id):
    profile = Profile.objects.get(id=id)
    if profile.user == request.user or profile.mode == 'public':

        users = Following.objects.filter(target=profile.user)
        followers = [line.follower.profile for line in users]
        context = {
            'followers':followers
        }
        follower_list = render_to_string('follower_list.html',context=context,request=request)
        return JsonResponse({'followers':follower_list})
    else:
        return JsonResponse({'followers':False})

def get_following_list_api_view(request,id):
    profile = Profile.objects.select_related('user').get(id=id)
    if profile.user == request.user or profile.mode == 'public':
        users = Following.objects.filter(follower=profile.user)
        followings = [line.target.profile for line in users]
        context = {
            'followers':followings
        }
        following_list = render_to_string('follower_list.html',context=context,request=request)
        return JsonResponse({'followings':following_list})
    else:
        return JsonResponse({'followings':False})

def get_post_list_api_view(request,id):
    profile = Profile.objects.select_related('user').get(id=id)
    if profile.user == request.user or profile.mode == 'public':
        posts = profile.post_set.all()
        context = {
            'posts':posts
        }
        post_list = render_to_string('post_list.html',context=context,request=request)
        return JsonResponse({'posts':post_list})
    else:
        return JsonResponse({'posts':False})  