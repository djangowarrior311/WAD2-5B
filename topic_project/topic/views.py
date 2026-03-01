from django.shortcuts import render
from django.http import HttpResponse

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
    