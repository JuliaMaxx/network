from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Post
from django.contrib.auth.decorators import login_required


def index(request):
    if request.method == "GET":
        posts = Post.objects.all()
        return render(request, "network/index.html", {
            "posts": posts.order_by('-time')
        })
    else:
        post = request.POST['post']
        new_post = Post(user=request.user, text=post)
        new_post.save()
        return HttpResponseRedirect(reverse("index"))



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
        if request.FILES['image']:
            image = request.FILES["image"]

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
            if image:
                user.image = image
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def profile(request, profile_id):
    user = User.objects.get(pk=profile_id)
    if request.method == 'GET':
        return render(request, "network/profile.html", {
            "user1":user, "posts": user.posts.order_by('-time')
        })
    else:
        if request.POST['followers'] == 'follow':
            user.followers.add(request.user)
            user.save()
        else:
            user.followers.remove(request.user)
            user.save()
        return HttpResponseRedirect(reverse("profile", args=(user.id, )))
    
@login_required
def following(request, profile_id):
    user = User.objects.get(pk=profile_id)
    following = user.following.all()
    posts = []
    for followed_user in following:
       posts += followed_user.posts.order_by('-time')

    return render (request, "network/following.html", {"posts":posts})