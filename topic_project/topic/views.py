from django.http import HttpResponse, HttpRequest, JsonResponse
from typing import TypedDict
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, EmailVerification, Tag, LearningTool, Review
from .forms import UserForm, ToolForm, ReviewForm
from .utils import send_verification_email
from django.contrib.auth.models import User
from django.urls import reverse

from django.db.models import Count, Q


import json


class TestContext(TypedDict):
    announcement: str


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    context_dict: TestContext = {
        "announcement": "Hello world!"
    }

    return render(request, "home.html", context=context_dict)

#add tool view
def addtool(request):
    form = ToolForm()
    
    if request.method == 'POST':
        form = ToolForm(request.POST)
        if form.is_valid():
            tool = form.save(commit=False)
            tool.creator = request.user 
            tool.save()
            return redirect('index') 
        else:
            print(form.errors)
            
    context = {'form': form}
    return render(request, 'topic/addtool.html', context=context)
    

# def test(request: HttpRequest):
    
# simple login and logout code

def user_login(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")


@login_required
def user_logout(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

# starting register path, takes in the users inputs
# after being checked by the js code
# redirects to the email verification if it works.

def register(request: HttpRequest) -> HttpResponse:
    registered = False
    if request.method == "POST":
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            request.session["registration_data"] = {
                "username": user_form.cleaned_data["username"],
                "email": user_form.cleaned_data["email"],
                "password": user_form.cleaned_data["password"],
            }
            email = user_form.cleaned_data["email"]
            send_verification_email(email)

            messages.success(request, "Verification code sent to your email.")
            return redirect("topic:verify_email")
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,
                "register.html",
                    context = {"user_form": user_form,
                                "registered": registered})

# attempts to verify the email given by checking the code given against the one sent
# will attempt to redirect user to either login if it worked or
# to resend the code or restart the form.

def verify_email(request: HttpRequest) -> HttpResponse:
    if "registration_data" not in request.session:
        messages.error(request, "Please start registration again.")
        return redirect("topic:register")
    
    email = request.session["registration_data"]["email"]

    if request.method == "POST":
        code = request.POST.get("code")

        try:
            verification = EmailVerification.objects.get(email = email, code = code)

            if verification.is_expired():
                messages.error(request, "Code expired. Please request a new one.")
                verification.delete()
                return redirect("topic:resend_code")
            
            user_data = request.session["registration_data"]

            user = User.objects.create_user(
                username=user_data["username"],
                email=user_data["email"],
                password=user_data["password"]
            )

            UserProfile.objects.create(user=user)
            verification.delete()
            request.session.flush()
            messages.success(request, "Registration complete! You can now log in.")
            return redirect("topic:login")
        
        except EmailVerification.DoesNotExist:
            messages.error(request, 'Invalid verification code')

    return render(request, 'verify_email.html', {'email': email})

# resends the code given the same email if the 
# code expired before the user could input it



def resend_code(request: HttpRequest) -> HttpResponse:
    if "registration_data" not in request.session:
        return redirect("topic:register")
    
    email = request.session["registration_data"]["email"]
    
    if request.method == "POST":
        send_verification_email(email)
        messages.success(request, "New verification code sent!")
        return redirect("topic:verify_email")
    
    return render(request, "resend_code.html", {"email": email})



# helper functions for the js code

def check_username(request: HttpRequest) -> JsonResponse:
    username = request.GET.get("username", "")
    
    if len(username) < 3:
        return JsonResponse({"available": False})
    
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({"available": not exists})


def check_email(request: HttpRequest) -> JsonResponse:
    email = request.GET.get("email", "")
    
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({"available": not exists})


def clamp(a: int, min: int, max: int):
    if a > max:
        return max
    elif a < min:
        return min
    return a


# getting tool results
MAX_RESULTS = 50

def get_search_results(request: HttpRequest) -> JsonResponse:
    query = request.GET.get("request", None)
    offset = request.GET.get("offset", "0")

    try:
        offset = int(offset)
    except ValueError:
        offset = 0

    if query is None:
        tools = LearningTool.objects.all()
    else:
        # can't use postgres' better search tools because of weird error '@'?
        tools = LearningTool.objects.filter(Q(description__icontains=query) | Q(name__icontains=query))

    # get count of results
    n_tools = tools.count()

    outputdata = []

    for i in tools[offset:MAX_RESULTS + offset]:
        outputdata.append({
            "name": i.name,
            "url": i.link,
            "review_slug": "topic/tools/" + i.slug,
            "tags": [j.name for j in i.tags.all()]
        })

    return JsonResponse({"data": outputdata,
                         "total": n_tools})
    
    
def get_tags(request: HttpRequest) -> JsonResponse:
    if request.method != "GET":
        return JsonResponse({"data": []})
    tags = Tag.objects.all()
    return JsonResponse({"data": [i.name for i in tags]})

@login_required
def add_review(request: HttpRequest, learning_tool_slug) -> HttpResponse:
    try:
        tool = LearningTool.objects.get(slug=learning_tool_slug)
    except LearningTool.DoesNotExist:
        tool = None
    if tool==None:
        return redirect('home')
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if tool:
                review = form.save(commit=False)
                review.user = request.user
                review.tool = tool
                review.save()
                return redirect(reverse('topic:show_tool',
                                        kwargs={'learning_tool_slug':
                                                learning_tool_slug}))
        else:
            print(form.errors)
    context_dict = {"form": form, "tool": tool}
    return render(request, "add_review.html", context=context_dict)

def show_tool(request: HttpRequest, learning_tool_slug) -> HttpResponse:
    context_dict = {}
    try:
        tool = LearningTool.objects.get(slug=learning_tool_slug)
        reviews = Review.objects.filter(tool=tool)
        context_dict['reviews'] = reviews
        context_dict['tool'] = tool
    except LearningTool.DoesNotExist:
        context_dict['reviews'] = None
        context_dict['tool'] = None
    return render(request, 'tool.html', context=context_dict)