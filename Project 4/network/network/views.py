from json import loads as load_json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow, Like

from .forms import NewPostForm


def index(request):
    return render(request, "network/index.html", {
        'form': NewPostForm(),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
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
    

def create(request):
    if request.method == "POST":
        request_body = load_json(request.body)
        content = request_body['content']
        new_post = Post(content=content, author=request.user)
        new_post.save()
        return JsonResponse({'result': 'success'})
        

def get_posts(request):
    if request.method == "POST":
        request_body = load_json(request.body)
        page = request_body['page']
        usernames = request_body['users']

        if usernames == None:
            paginator = Paginator(Post.objects.all().order_by('-timestamp'), 10)
            posts = Paginator(Post.objects.all().order_by('-timestamp'), 10).page(page).object_list
        else:
            users = map(lambda username: User.objects.get(username=username), usernames)
            paginator = Paginator(Post.objects.filter(author__in=users).order_by('-timestamp'), 10)

        posts = paginator.page(page).object_list
        response = {'pages': paginator.num_pages, 'posts': {}}

        for i, post in enumerate(posts):
            response['posts'][f'post_{i + 1}'] = post.serialize(request.user if request.user.is_authenticated else None)
        
        return JsonResponse(response)
    

def profile(request, username):
    user = User.objects.get(username=username)
    if request.user.is_authenticated:
        is_followed = len(Follow.objects.filter(follower=request.user, followee=user)) == 1
    else:
        is_followed = False
    return render(request, "network/profile.html", {
        'viewed_user': user,
        'follow_button': "Unfollow" if is_followed else "Follow",
        'followers': len(Follow.objects.filter(followee=user)),
        'following': len(Follow.objects.filter(follower=user)),
    })
    

def follow(request):
    if request.method == "POST":
        request_body = load_json(request.body)
        user = User.objects.get(username=request_body['username'])
        is_followed = len(Follow.objects.filter(follower=request.user, followee=user)) == 1
        followers = len(Follow.objects.filter(followee=user))
        if is_followed:
            Follow.objects.get(follower=request.user, followee=user).delete()
            return JsonResponse({'result': 'unfollowed', 'followers': followers - 1})
        else:
            follow = Follow(follower=request.user, followee=user)
            follow.save()
            return JsonResponse({'result': 'followed', 'followers': followers + 1})
        

def get_followers(request):
    if request.method == "POST":
        followers = map(lambda follow: follow.followee.username, Follow.objects.filter(follower=request.user))
        return JsonResponse({'followers': list(followers)})
    

def following(request):
    return render(request, "network/following.html", {
        
    })


def like(request):
    if request.method == "POST":
        request_body = load_json(request.body)
        post = Post.objects.get(id=request_body['post_id'])
        is_liked = len(Like.objects.filter(post=post, liker=request.user)) == 1
        likes = len(Like.objects.filter(post=post))
        if is_liked:
            Like.objects.get(post=post, liker=request.user).delete()
            return JsonResponse({'result': 'unliked', 'likes': likes - 1})
        else:
            like = Like(post=post, liker=request.user)
            like.save()
            return JsonResponse({'result': 'liked', 'likes': likes + 1})
        

def edit_post(request):
    if request.method == "POST":
        request_body = load_json(request.body)
        post = Post.objects.get(id=request_body['post_id'])
        if request.user == post.author:
            post.content = request_body['new_content']
            post.save()
            return JsonResponse({'result': 'success'})