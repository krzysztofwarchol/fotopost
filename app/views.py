from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
from app.ml_model.ml_model import predict_tags
from app.recommendation.recommend import recommend_users
from app.face_recognition.detection import FaceRecognition

from .models import *

faceRecognition = FaceRecognition()


def index(request):
    all_posts = Post.objects.all().order_by("-date_created")

    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get("page")
    if page_number == None:
        page_number = 1
    posts = paginator.get_page(page_number)
    followings = []
    suggestions = []
    if request.user.is_authenticated:

        suggestions = recommend_users(request.user.id)

    return render(
        request,
        "index.html",
        {
            "posts": posts,
            "suggestions": suggestions,
            "page": "all_posts",
            "profile": False,
        },
    )


def facelogin(request):
    face_id = faceRecognition.recognizeFace()

    if face_id == None:
        return HttpResponseRedirect(reverse("login"))
    else:
        user = User.objects.get(id=face_id)
        login(request, user)
        return HttpResponseRedirect(reverse("index"))


def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request, "login.html", {"message": "Invalid username and/or password."}
            )
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def validate_password(password):
    if len(password) < 12:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char in set("[~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-=") for char in password):
        return False
    return True


def addFace(face_id):
    face_id = face_id
    faceRecognition.faceDetect(face_id)
    faceRecognition.trainFace()


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        profile = request.FILES.get("profile")

        cover = request.FILES.get("cover")

        password = request.POST["password"]
        if not validate_password(password) or username in password:
            return render(
                request,
                "register.html",
                {
                    "message2": "Password must be at least 12 characters long and contain at least one lowercase letter, one uppercase letter, one digit, and one special character and must not contain the username."
                },
            )

        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "register.html", {"message": "Passwords must match."}
            )

        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            if profile is not None:
                user.profile_pic = profile
            else:
                user.profile_pic = "default_profile_picture.png"
            if cover is not None:
                user.cover = cover
            else:
                user.cover = "default_cover.png"
            user.bio = "default bio"
            user.save()
            Follower.objects.create(user=user)

        except IntegrityError:
            return render(
                request, "register.html", {"message": "Username already taken."}
            )
        try:
            addFace(user.id)
        except:
            print("Error face scan")

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


def profile(request, username):
    user = User.objects.get(username=username)
    all_posts = Post.objects.filter(creater=user).order_by("-date_created")
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get("page")
    if page_number == None:
        page_number = 1
    posts = paginator.get_page(page_number)
    followings = []
    suggestions = []
    follower = False
    if request.user.is_authenticated:

        suggestions = recommend_users(request.user.id)

        if request.user in Follower.objects.get(user=user).followers.all():
            follower = True

    follower_count = Follower.objects.get(user=user).followers.all().count()
    following_count = Follower.objects.filter(followers=user).count()
    return render(
        request,
        "profile.html",
        {
            "username": user,
            "posts": posts,
            "posts_count": all_posts.count(),
            "suggestions": suggestions,
            "page": "profile",
            "is_follower": follower,
            "follower_count": follower_count,
            "following_count": following_count,
        },
    )


def profile_edit(request, username):
    user = User.objects.get(username=username)

    if request.user.is_authenticated:
        if request.method == "POST":

            fname = request.POST["firstname"]

            lname = request.POST["lastname"]

            bio = request.POST["bio"]

            profile = request.FILES.get("profile")

            cover = request.FILES.get("cover")

            password = request.POST["password"]

            try:
                if fname != "":
                    user.first_name = fname
                if lname != "":
                    user.last_name = lname
                if bio != "":
                    user.bio = bio
                if profile != None:
                    user.profile_pic = profile
                if cover != None:
                    user.cover = cover
                if password != "":
                    if not validate_password(password) or username in password:
                        return render(
                            request,
                            "profile_edit.html",
                            {
                                "message2": "Password must be at least 12 characters long and contain at least one lowercase letter, one uppercase letter, one digit, and one special character and must not contain the username."
                            },
                        )

                    confirmation = request.POST["confirmation"]
                    if password != confirmation:
                        return render(
                            request,
                            "profile_edit.html",
                            {"message": "Passwords must match."},
                        )
                    user.set_password(password)

                user.save()
            except IntegrityError:
                return render(
                    request,
                    "profile_edit.html",
                    {"username": user, "message": "Data has not been changed"},
                )

            return HttpResponseRedirect(reverse("index"))

        return render(
            request,
            "profile_edit.html",
            {
                "username": user.username,
            },
        )
    else:
        return HttpResponseRedirect(reverse("login"))


def tag(request, name_tag):
    if request.user.is_authenticated:
        tag = Tag.objects.get(name_tag=name_tag)

        all_posts_tag = PostTag.objects.filter(tag_id=tag.id).values_list(
            "post_id", flat=True
        )

        all_posts = []

        for post_id in all_posts_tag:

            all_posts.append(Post.objects.get(id=post_id))

        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get("page")
        if page_number == None:
            page_number = 1
        posts = paginator.get_page(page_number)

        suggestions = recommend_users(request.user.id)

        return render(
            request,
            "index.html",
            {
                "posts": posts,
                "name_tag": name_tag,
                "suggestions": suggestions,
                "page": "tag",
            },
        )
    else:
        return HttpResponseRedirect(reverse("login"))


def following(request):
    if request.user.is_authenticated:
        following_user = Follower.objects.filter(followers=request.user).values("user")
        all_posts = Post.objects.filter(creater__in=following_user).order_by(
            "-date_created"
        )

        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get("page")
        if page_number == None:
            page_number = 1
        posts = paginator.get_page(page_number)

        suggestions = recommend_users(request.user.id)

        return render(
            request,
            "index.html",
            {"posts": posts, "suggestions": suggestions, "page": "following"},
        )
    else:
        return HttpResponseRedirect(reverse("login"))


def saved(request):
    if request.user.is_authenticated:
        all_posts = Post.objects.filter(savers=request.user).order_by("-date_created")

        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get("page")
        if page_number == None:
            page_number = 1
        posts = paginator.get_page(page_number)

        suggestions = recommend_users(request.user.id)

        return render(
            request,
            "index.html",
            {"posts": posts, "suggestions": suggestions, "page": "saved"},
        )
    else:
        return HttpResponseRedirect(reverse("login"))


@login_required
def create_post(request):
    if request.method == "POST":
        text = request.POST.get("text")

        pic = request.FILES.get("picture")

        try:
            post = Post.objects.create(
                creater=request.user, content_text=text, content_image=pic
            )
            post_id = post.id
            if pic != None:

                tags = predict_tags(post.content_image)
                class_dict = {
                    "house": 1,
                    "birds": 2,
                    "sun": 3,
                    "valley": 4,
                    "nighttime": 5,
                    "boats": 6,
                    "mountain": 7,
                    "tree": 8,
                    "snow": 9,
                    "beach": 10,
                    "vehicle": 11,
                    "rocks": 12,
                    "reflection": 13,
                    "sunset": 14,
                    "road": 15,
                    "flowers": 16,
                    "ocean": 17,
                    "lake": 18,
                    "window": 19,
                    "plants": 20,
                    "buildings": 21,
                    "grass": 22,
                    "water": 23,
                    "animal": 24,
                    "person": 25,
                    "clouds": 26,
                    "sky": 27,
                    "not detected": 28,
                }
                tags = list(map(class_dict.get, tags))
                for tag in tags:
                    post_obj = Post.objects.get(id=post_id)
                    tag_obj = Tag.objects.get(id=tag)
                    post_tag = PostTag.objects.create(post=post_obj, tag=tag_obj)
                    post_tag.save()
            return HttpResponseRedirect(reverse("index"))
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Method must be 'POST'")


@csrf_exempt
def like_post(request, id):
    if request.user.is_authenticated:
        if request.method == "PUT":
            post = Post.objects.get(pk=id)

            try:
                post.likers.add(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
def unlike_post(request, id):
    if request.user.is_authenticated:
        if request.method == "PUT":
            post = Post.objects.get(pk=id)

            try:
                post.likers.remove(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
def save_post(request, id):
    if request.user.is_authenticated:
        if request.method == "PUT":
            post = Post.objects.get(pk=id)
            try:
                post.savers.add(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
def unsave_post(request, id):
    if request.user.is_authenticated:
        if request.method == "PUT":
            post = Post.objects.get(pk=id)
            try:
                post.savers.remove(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
def follow(request, username):
    if request.user.is_authenticated:
        if request.method == "PUT":
            user = User.objects.get(username=username)

            try:
                (follower, create) = Follower.objects.get_or_create(user=user)
                follower.followers.add(request.user)
                follower.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
def unfollow(request, username):
    if request.user.is_authenticated:
        if request.method == "PUT":
            user = User.objects.get(username=username)

            try:
                follower = Follower.objects.get(user=user)
                follower.followers.remove(request.user)
                follower.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
def comment(request, post_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = json.loads(request.body)
            comment = data.get("comment_text")
            post = Post.objects.get(id=post_id)
            try:
                newcomment = Comment.objects.create(
                    post=post, commenter=request.user, comment_content=comment
                )
                post.comment_count += 1
                post.save()

                return JsonResponse([newcomment.serialize()], safe=False, status=201)
            except Exception as e:
                return HttpResponse(e)

        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post)
        comments = comments.order_by("-comment_time").all()
        return JsonResponse([comment.serialize() for comment in comments], safe=False)
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
def delete_post(request, post_id):
    if request.user.is_authenticated:
        if request.method == "PUT":
            post = Post.objects.get(id=post_id)
            if request.user == post.creater:
                try:
                    delet = post.delete()
                    return HttpResponse(status=201)
                except Exception as e:
                    return HttpResponse(e)
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse("login"))
