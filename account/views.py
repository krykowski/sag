from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext

from utils import render_to

from account.forms import UserCreateForm

@render_to('account/create.html')
def register(request):
    if request.method == 'GET':
        form = UserCreateForm()
    else:
        form = UserCreateForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            print user
            login(user, request)
            redirect(user)
            
    return {'form': form}