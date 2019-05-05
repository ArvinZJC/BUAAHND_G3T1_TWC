'''
Xadmin configuration for the app "users";
@author: Liu Haodong and Wang Annong
'''

from .models import UserProfile, EmailVerifyRecord
import xadmin
from xadmin import views


#inherited from class object instead of class admin to use Xadmin

class BaseSettings(object):
    '''
    Configure base settings for the site.
    '''
    
    use_bootswatch = True


class GlobalSettings(object):
    '''
    Configure global settings for the site.
    '''
    
    site_title = 'Patient Registration System'
    site_footer = '2018 Team G'
    menu_style = 'accordion'


class UserProfileAdmin(object):
    '''
    Configuration for the label "User profile(s)" in the category "User Centre".
    '''
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'gender', 'birthday', 'mobile', 'last_login']
    search_fields = ['username', 'first_name', 'last_name', 'gender', 'mobile']
    list_filter = ['username', 'email', 'image', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active', 'gender', 'birthday', 'mobile', 'date_joined', 'last_login']
    readonly_fields = ['is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login']
    show_bookmarks = False
    model_icon = 'glyphicon glyphicon-user'
    
    def queryset(self):
        '''
        Control of the user profile displayed according to the user permissions.
        '''
        
        user_profile = super(UserProfileAdmin, self).queryset()
        
        # an administrator can view all the user profiles
        if self.request.user.is_superuser:
            return user_profile
        # a doctor or on ordinary user can only view his/her own user profile
        else:
            return user_profile.filter(username = self.request.user.username)
    

class EmailVerifyRecordAdmin(object):
    '''
    Configuration for the label "Email verification record(s)" in the category "User Centre".
    '''
    
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    show_bookmarks = False
    model_icon = 'glyphicon glyphicon-envelope'


# register classes with their managers
xadmin.site.unregister(UserProfile)  # class UserProfile cannot be later registered with class UserProfileAdmin unless class UserProfile is unregistered
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)