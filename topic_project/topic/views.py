from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from typing import TypedDict
from topic.forms import ToolForm

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
    