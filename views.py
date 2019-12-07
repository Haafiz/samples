from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404
from django import urls
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from accounts.forms import UserRegistrationForm, UserProfileForm,\
    CompanyRegistrationForm
from pprint import pprint
from django.http import HttpResponse
from accounts.forms import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import logout



def register(request,template_name="account/register.html"):
    if request.method=='POST':
        postdata=request.POST.copy()
        form=UserRegistrationForm(postdata)
        if form.is_valid():
            form.save()
            em=postdata.get('email','')
            pw=postdata.get('password1','')
            from django.contrib.auth import login,authenticate
            new_user=authenticate(username=em,password=pw)
            if new_user and new_user.is_active:
                login(request,new_user)
                url=url.reverse('dashboard')
                return HttpResponseRedirect(url)     
    else:
        form=UserRegistrationForm()
    page_title="User Registration"
    return render(request, template_name,locals())
        
def logout(request):
    logout(request)

def ask_email_verification(request,template_name="account/ask_email_verification.html"):
    return render(request, template_name,locals())

def profile(request):
    if request.user.get_profile().company:
        from company import views
        return views.profile(request)
    else:
        pass
    
def company_register(request,template_name="account/register.html"):
    if request.method=='POST':
        postdata=request.POST.copy()
        form=CompanyRegistrationForm(postdata)
        if form.is_valid():
            form.save()
            em=postdata.get('email','')
            pw=postdata.get('password1','')
            from django.contrib.auth import login,authenticate
            new_user=authenticate(username=em,password=pw)
            if new_user and new_user.is_active:
                login(request,new_user)
                url=urlresolvers.reverse('dashboard')
                return HttpResponseRedirect(url)
    else:
        form=CompanyRegistrationForm()
    page_title="User Registration"
    return render(request, template_name,locals())

@login_required
def dashboard(request,template_name="account/dashboard.html"):
    return HttpResponse(request.user.get_profile().company)
    return HttpResponse(request.user.get_profile().company.full_name)

@login_required
def settings(request):
    pass

def forgot_password(request):
    pass

def logged_out(request,template_name='account/logged_out.html'):
    return render(request, template_name, locals())

def activate(request,activation_key):
    userp=UserProfile.objects.get(activation_key=activation_key)
    user_email=userp.user.email
    active_user_count=User.objects.filter(is_active=1,email=user_email).count()
    if active_user_count:
        pass
    else:
        userp.user.is_active=True
    userp.user.save()
    return HttpResponseRedirect(urlresolvers.reverse('login')+"?vf=1")