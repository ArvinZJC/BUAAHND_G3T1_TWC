'''
users/forms.py:
it contains forms of this app

created on 23 October, 2018

@author: Liu Haodong and Wang Annong
'''

from django import forms
from captcha.fields import CaptchaField


class LoginForm( forms.Form ):
    '''
    Define the login verification form.
    '''
    
    username = forms.CharField( required = True )
    password = forms.CharField( required = True, min_length = 6 )


class RegisterForm( forms.Form ):
    '''
    Define the sign-up verification form.
    '''
    
    email = forms.EmailField( required = True )
    password = forms.CharField( required = True, min_length = 6 )
    captcha = CaptchaField( error_messages = { 'invalid': 'Incorrect captcha!' } )


class ForgetPwdForm( forms.Form ):
    '''
    Define the form for getting back a password.
    '''
    
    email = forms.EmailField( required = True )
    captcha = CaptchaField( error_messages = { 'invalid': 'Incorrect captcha!' } )


class ModifyPwdForm( forms.Form ):
    '''
    Define the form for resetting a password
    '''
    
    password1 = forms.CharField( required = True, min_length = 6 )
    password2 = forms.CharField( required = True, min_length = 6 )