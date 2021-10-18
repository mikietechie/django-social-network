from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import *
import json
from django.views.decorators.csrf import csrf_exempt


def index(request):
    context = {}
    context['header'] = "All posts"
    posts = (Post.objects.all())[::-1]
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    context['posts'] = paginator.get_page(page_number)
    return render(request, "network/index.html",context=context)

@login_required(login_url='login')
def new_view(request):
    context = {}
    if request.method == 'POST':
        user = User.objects.get(username = request.POST['username'])
        msg = request.POST['msg']
        post = Post(user=user,msg=msg)
        post.save()
        context['msg'] = 'Post successfull'
        return render(request,"network/new.html",context=context)
    return render(request,"network/new.html",context=context)

@login_required(login_url='login')
def profile_view(request):
    try:
        you = User.objects.get(username=request.session['username'])
        profile_user = User.objects.get(username=request.GET.get('username'))
    except:
        return render(request, 'network/error.html',{'error_msg':"Sorry user does not exist"})
    if request.GET.get('action') == 'follow':
        try:
            Follow.objects.get(user=profile_user,follower=you)
        except:
            new_follower = Follow(user=profile_user,follower=you)
            new_follower.save()
    if request.GET.get('action') == 'unfollow':
        try:
            follower = Follow.objects.get(user=profile_user,follower=you)
            follower.delete()
        except:
            pass
    followers = Follow.objects.filter(user=profile_user).count()
    following = Follow.objects.filter(follower=profile_user).count()
    posts = (Post.objects.filter(user=profile_user))[::-1]
    posts_num = Post.objects.filter(user=profile_user).count()
    context = {
        'profile_user':profile_user,
        'followers':followers,
        'following':following,
        'posts_num':posts_num
    }
    context['is_self'] = request.GET.get('username') == request.session['username']
    try:
        Follow.objects.get(user=profile_user,follower=you)
        context['is_follower']  = True
    except:
        context['is_follower'] = False
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    context['posts'] = paginator.get_page(page_number)
    return render(request,"network/profile.html",context=context)

@login_required(login_url='login')
def following_view(request):
    profile_user = User.objects.get(username=request.session['username'])
    posts = []
    following = profile_user.follower.all()
    for follow in following:
        if follow.user.poster.all().count()>0:
            for post in follow.user.poster.all():
                posts.append(post)
            
    context = {}
    posts.sort(key=lambda post: post.timestamp)
    posts.reverse()
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    context['posts'] = paginator.get_page(page_number)
    return render(request,"network/following.html",context=context)

@csrf_exempt
@login_required(login_url='login')
def post(request,id):
    if request.method == "PUT":
        try:
            post = Post.objects.get(pk=id)
        except:
            return JsonResponse({"error": "post not found."}, status=404)
        data = json.loads(request.body)
        if data.get('like') is not None:
            opinion = 'opinion'+str(post.id)
            if request.session.get(opinion) is None:
                post.likes = post.likes+1
                post.save()
                request.session[opinion] = 1
                return JsonResponse(post.serialize())
            else:
                return JsonResponse(post.serialize())
        if data.get('dislike') is not None:
            opinion = 'opinion'+str(post.id)
            if request.session.get(opinion) is None:
                post.dislikes = post.dislikes+1
                post.save()
                request.session[opinion] = 1
                return JsonResponse(post.serialize())
            else:
                return JsonResponse(post.serialize())
        if data.get('msg') is not None:
            if request.session['username'] == post.user.username:
                post.msg = data['msg']
                post.save()
                return JsonResponse(post.serialize())
            else:
                return JsonResponse(post.serialize())


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
