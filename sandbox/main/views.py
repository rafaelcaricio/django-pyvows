from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm


def home(request):
    return HttpResponse('hello world')


def say_hello(request):
    SAY_HELLO_WITHOUT_NAME = getattr(settings, "SAY_HELLO_WITHOUT_NAME", False)
    if 'name' in request.GET:
        name = request.GET['name']
    elif SAY_HELLO_WITHOUT_NAME:
        name = 'guest'
    else:
        return HttpResponse("What's your name?")
    return HttpResponse("Hello, %s!" % name)


def post_it(request):
    return HttpResponse(request.POST['value'])


def post_file(request):
    return HttpResponse(request.FILES['the_file'].read().strip())


def post_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect(
                    '/say/?name={}'.format(form.cleaned_data['your_name']))

    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form})
