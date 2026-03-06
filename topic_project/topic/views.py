from django.shortcuts import render
from django.http import HttpResponse
from topic.forms import UserForm
from django.http import HttpRequest
from typing import TypedDict


class TestContext(TypedDict):
    announcement: str


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    context_dict: TestContext = {
        "announcement": "Hello world!"
    }

    return render(request, "home.html", context=context_dict)


# def test(request: HttpRequest):
    



def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,
                'register.html',
                    context = {'user_form': user_form,
                                'registered': registered})