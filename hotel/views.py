from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import NewUserForm

# Create your views here.
def user_register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else: 
        form = NewUserForm()
    return render (request=request, template_name="registration/register.html", context={"form":form})

def index(request):
    return render (request=request, template_name="index.html")
