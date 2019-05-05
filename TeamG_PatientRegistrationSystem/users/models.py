'''
originally generated by "django-admin startapp" using Django 2.1.7 for the app "users";
it contains structures of tables UserProfile and EmailVerifyRecord in the database;
@author: Liu Haodong and Wang Annong
'''

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class UserProfile(AbstractUser):
    '''
    Table UserProfile storing personal information.
    Inherited from class AbstractUser which includes attributes username, password, and so on with functions get_full_name, check_password, and etc.
    '''
    
    gender_choices = (
        ('1', 'Male'),
        ('2', 'Female')
    )
    
    is_staff = models.BooleanField(default = True)
    gender = models.CharField('gender', max_length = 10, choices = gender_choices, default = '1')
    birthday = models.DateField('birthday', null = True, blank = True)
    mobile = models.CharField('mobile', max_length = 20, null = True, blank = True)
    image = models.ImageField('head image', upload_to = 'head', default = 'head/default.png', max_length = 200)  # field for the user avatar
    
    class Meta:
        verbose_name = 'User profile'
    
    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    '''
    Table EmailVerifyRecord storing email verification records.
    '''
    
    type_choices = (
        ('1', 'Sign up'),
        ('2', 'Reset password'),
        ('3', 'Change an email address')
    )
    
    code = models.CharField('verification code', max_length = 20)
    email = models.EmailField('email', max_length = 50)
    send_type = models.CharField('type', choices = type_choices, default = '1', max_length = 30)
    send_time = models.DateTimeField('post time', default = timezone.now)
    
    class Meta:
        verbose_name = 'Email verification record'