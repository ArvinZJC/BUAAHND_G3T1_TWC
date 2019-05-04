'''
users/views.py:
originally generated by "django-admin startapp" using Django 2.1.2 for the app "users"
it contains views of this app

created on 23 October, 2018

@author: Liu Haodong and Wang Annong
'''

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm
from utils.email_send import send_register_eamil


class CustomBackend( ModelBackend ):
    '''
    The user can log in with either the username or the verified email address.
    Inherited from class ModelBackend which includes function authenticate.
    '''
    
    def authenticate( self, username = None, password = None ):
        '''
        Authenticate to enable that the user can log in with either the username or the verified email address.
        '''
        
        try:
            user = UserProfile.objects.get( Q( username = username ) | Q( email = username ) )  #the username and verified email address should represent the same account
            
            '''
            call the specified function in class UserProfile inherited from class AbstractUser to verify the password entered
            the password on the back end of Django is encrypted so it is wrong to use "password == password" as the condition
            '''
            if user.check_password( password ):
                return user
        except:
            return None


class LoginView( View ):
    '''
    The user tries to log in.
    '''
    
    def get( self, request ):
        return render( request, 'login.html' )

    def post( self, request ):
        login_form = LoginForm( request.POST )  #create a LoginForm object and assign it to "login_form"
        
        if login_form.is_valid():
            username_entered = login_form.cleaned_data[ 'username' ]  #get the username submitted by the user
            password_entered = login_form.cleaned_data[ 'password' ]  #get the password submitted by the user
            authentication = CustomBackend()
            user = authentication.authenticate( username = username_entered, password = password_entered )  #return a User object if the username and password entered are valid, or return None
            
            #execute if the username and password entered are valid
            if user is not None:
                #execute if the account is activated by email
                if user.is_active:
                    login( request, user )
                    return HttpResponseRedirect( reverse( 'home' ) )
                else:
                    return render( request, 'login.html', { 'error_message': 'Your email address has not yet been verified.', 'login_form': login_form } )
            #execute if the username and password entered are invalid
            else:
                return render( request, 'login.html', { 'error_message': 'Incorrect username or password!', 'login_form': login_form } )
        else:
            return render( request, 'login.html', { 'login_form': login_form } )


class ActiveUserView( View ):
    '''
    The user tries to activate an account.
    '''
    
    def get( self, request, active_code ):
        all_record = EmailVerifyRecord.objects.filter( code = active_code )  #get all attributes of the specified email verification record if the record exists
        
        #execute if the specified email verification record exists
        if all_record:
            for record in all_record:
                user = UserProfile.objects.get( email = record.email )  #find the owner of the specified email address from table UserProfile
                user.is_active = True
                user.save()
                
                try:
                    ordinary_user = Group.objects.filter( name = 'Ordinary Users' ).first()
                    user.groups.add( ordinary_user )  #add the new user to the default group "Ordinary users"
                except:
                    pass
        else:
            return render( request, 'active_fail.html' )  #turn to the bad activation page if the verification fails
        
        return HttpResponseRedirect( reverse( 'login' ) )  #turn to the login page if the account is activated successfully


class RegisterView( View ):
    '''
    The user tries to sign up.
    '''
    
    def get( self, request ):
        register_form = RegisterForm()  #create a RegisterForm object and assign it to "register_form"
        return render( request, 'sign-up.html', { 'register_form': register_form } )

    def post( self, request ):
        register_form = RegisterForm( request.POST )  #create a RegisterForm object and assign it to "register_form"
        
        if register_form.is_valid():
            username_entered = request.POST.get( 'email', None )
            
            if UserProfile.objects.filter( email = username_entered ):
                return render( request, 'sign-up.html', { 'register_form': register_form, 'error_message': 'The email address already exists.' } )

            password_entered = request.POST.get( 'password', None )
            user_profile = UserProfile()  #create a UserProfile object and assign it to "user_profile"
            
            user_profile.username = username_entered
            user_profile.email = username_entered
            user_profile.is_active = False  #the account will not be activated until the email is verified
            
            user_profile.password = make_password( password_entered )  #encrypt the password and save it
            user_profile.save()
            send_register_eamil( username_entered, '1' )  #call the specified function in module email_send of package utils to send a verification link to the specified email
            return render( request, 'send_success.html' )
        else:
            return render( request, 'sign-up.html', { 'register_form': register_form } )


class ForgetPwdView( View ):
    '''
    The user tries to get back a password.
    '''
    
    def get( self, request ):
        forget_form = ForgetPwdForm()  #create a ForgetPwdForm object and assign it to "forget_form"
        return render( request, 'forgetpwd.html', { 'forget_form': forget_form } )

    def post( self, request ):
        forget_form = ForgetPwdForm( request.POST )  #create a ForgetPwdForm object and assign it to "forget_form"
        
        if forget_form.is_valid():
            email = request.POST.get( 'email', None )
            send_register_eamil( email, '2' )  #call the specified function in module email_send of package utils to send a verification link to the specified email
            return render( request, 'send_success.html' )
        else:
            return render( request, 'forgetpwd.html', { 'forget_form': forget_form } )


class ResetView( View ):
    '''
    The user tries to reset a password.
    '''
    
    def get( self, request, active_code ):
        all_records = EmailVerifyRecord.objects.filter( code = active_code )  #get all attributes of the specified email verification record if the record exists
        
        #execute if the specified email verification record exists
        if all_records:
            for record in all_records:
                return render( request, 'password_reset.html', { 'email': record.email } )
        else:
            return render( request, 'active_fail.html' )
        
        return render( request, 'login.html' )


class ModifyPwdView( View ):
    '''
    The user tries to modify the password reset.
    '''
    
    def post( self, request ):
        modify_form = ModifyPwdForm( request.POST )  #create a ModifyPwdForm object and assign it to "modify_form"
        
        if modify_form.is_valid():
            pwd1 = request.POST.get( 'password1', '' )
            pwd2 = request.POST.get( 'password2', '' )
            email_entered = request.POST.get( 'email', '' )
            
            if pwd1 != pwd2:
                return render( request, 'password_reset.html', { 'email': email_entered, 'error_message': 'The two passwords you entered do not match.' } )
            
            user = UserProfile.objects.get( email = email_entered )
            user.password = make_password( pwd2 )
            user.save()
            return HttpResponseRedirect( reverse( 'login' ) )  #turn to the login page if the account is activated successfully
        else:
            email_entered = request.POST.get( 'email', '' )
            return render( request, 'password_reset.html', { 'email': email_entered, 'modify_form': modify_form } )


class LogoutView( View ):
    '''
    The user tries to log out.
    '''
    
    def get( self, request ):
        logout( request )
        return HttpResponseRedirect( reverse( 'index' ) )