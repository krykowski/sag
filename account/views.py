#-*- coding: utf-8 -*-

from django.contrib import auth
from django.shortcuts import redirect
from django.template.context import RequestContext

from utils import render_to

from account.forms import UserCreateForm, UserLoginForm, UserUpdateForm

@render_to('account/account.html')
def account(request):
    if request.method == 'GET':
        form = UserUpdateForm(instance=request.user)
    else:
        form = UserUpdateForm(request.POST, instance=request.user)
        
        if form.is_valid():
            ins = request.user
            ins.first_name = form.cleaned_data['first_name']
            ins.last_name = form.cleaned_data['last_name']
            ins.username = form.cleaned_data['username']
            ins.email = form.cleaned_data['email']
            
            if form.cleaned_data['password']:
                ins.set_password(form.cleaned_data['password'])
                
            ins.save()
            
    return {'form': form}

def logout(request):
    auth.logout(request)
    
    return redirect('/')

@render_to('pages/index.html')
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        
        if form.is_valid():
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            
            if user is not None:
                auth.login(request, user)
            
                return redirect('account.views.account')
            else:
                # dodaj do msg
                pass
        else:
            # dodaj do msg
            pass
        
    return {}

@render_to('account/create.html')
def register(request):
    if request.method == 'GET':
        form = UserCreateForm()
    else:
        form = UserCreateForm(request.POST, request.FILES)
        
        if form.is_valid():
            user = form.save(False)
            user.set_password(request.POST['password'])
            user.save()
            
            authUser = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            
            if authUser is not None:
                auth.login(request, authUser)
            
                return redirect('account.views.account')
            
    return {'form': form}