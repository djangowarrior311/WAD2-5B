from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib import messages
from .models import UserProfile, EmailVerification
from .forms import UserForm
from .utils import send_verification_email
from typing import TypedDict
from django.contrib.auth.models import User


class TestContext(TypedDict):
    announcement: str


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    context_dict: TestContext = {
        "announcement": "Hello world!"
    }

    return render(request, "home.html", context=context_dict)


# def test(request: HttpRequest):
    

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

            # change back to this when login is created
            # return redirect("topic:login")

            return redirect("topic:home")
        
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