'''
module that contains functions related to email verification

created on 30 October, 2018

@author: Liu Haodong and Zhao Jichen
'''

from random import Random

from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from PRS.settings import EMAIL_HOST_USER

def random_str( random_length = 8 ):
    '''
    Generate a random string.
    '''
    
    result = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'  #generate a random string using the following characters
    
    length = len( chars ) - 1
    random = Random()
    
    for counter in range( random_length ):
        result += chars[ random.randint( 0, length ) ]
    
    return result

def send_register_eamil( email, send_type = "1" ):
    '''
    Send a verification link/code.
    For "send_type", 1 means "Sign up", 2 means "Forgot password?", and 3 means "Change your email address"
    '''
    
    email_record = EmailVerifyRecord()  #create an EmailVerifyRecord object and assign it to "email_record"
    
    if send_type == '3':
        code = random_str( 4 )  #call the specified function to generate a verification code with 4 characters
    else:
        code = random_str( 16 )  #call the specified function to generate the keyword of a verification link with 16 characters
    
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    
    email_record.save()
    
    #identify the email content
    if send_type == '1':
        email_title = 'Please verify your email address'
        email_body = 'Dear Customer,\n\nYou recently created an account with {0}.\nTo confirm your email address, please click on this link:\nhttp://127.0.0.1:8000/active/{1}\n\nPlease note:\nIf you cannot access this link, copy and paste the entire URL into your browser.\n\nTeam G'.format( email, code )
        
        send_status = send_mail( email_title, email_body, EMAIL_HOST_USER, [ email ] )
        
        if send_status:
            pass
    elif send_type == '2':
        email_title = 'Please reset your password'
        email_body = 'Dear Customer,\n\nYou recently asked for resetting your password.\nTo complete the process, please click on this link:\nhttp://127.0.0.1:8000/reset/{0}\n\nPlease note:\nIf you cannot access this link, copy and paste the entire URL into your browser.\n\nTeam G'.format( code )
        
        send_status = send_mail( email_title, email_body, EMAIL_HOST_USER, [ email ] )
        
        if send_status:
            pass
    elif send_type == '3':
        email_title = 'Please verify your email address'
        email_body = 'Dear Customer,\n\nYou recently asked for changing your email address.\nTo continue the process, the following verification code is needed:\n{0}\n\nPlease note:\nNever share the code with others!\n\nTeam G'.format( code )
        
        send_status = send_mail( email_title, email_body, EMAIL_HOST_USER, [ email ] )
        
        if send_status:
            pass