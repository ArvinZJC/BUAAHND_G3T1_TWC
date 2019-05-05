'''
Xadmin configuration for the app "hospitals";
@author: Zhao Jichen and Ye Yifan
'''

from .models import HospitalInfo, DepartmentInfo, DoctorInfo, RegistrationInfo
import xadmin
from django.core.exceptions import ObjectDoesNotExist


# inherited from class object instead of class admin to use Xadmin

class HospitalInfoAdmin(object):
    '''
    Configuration for the label "Hospital(s)" in the category "Medical Service".
    '''
    
    list_display = ['name', 'brief_introduction', 'detail', 'address', 'director', 'tel']
    search_fields = ['name', 'brief_introduction', 'detail', 'address', 'director', 'tel']
    list_filter = ['name', 'brief_introduction', 'detail', 'address', 'director', 'tel']
    relfield_style = 'fa-ajax'
    show_bookmarks = False
    model_icon = 'glyphicon glyphicon-plus-sign'


class DepartmentInfoAdmin(object):
    '''
    Configuration for the label "Department(s)" in the category "Medical Service".
    '''
    
    list_display = ['name', 'belong_to', 'brief_introduction', 'detail', 'director', 'tel']
    search_fields = ['name', 'brief_introduction', 'detail', 'director', 'tel']
    list_filter = ['name', 'belong_to', 'brief_introduction', 'detail', 'director', 'tel']
    relfield_style = 'fa-ajax'
    show_bookmarks = False
    model_icon = 'glyphicon glyphicon-th'


class DoctorInfoAdmin(object):
    '''
    Configuration for the label "Doctor(s)" in the category "Medical Service".
    '''
    
    list_display = ['get_real_name', 'username', 'belong_to', 'brief_introduction', 'detail', 'is_available', 'is_expert']
    search_fields = ['brief_introduction', 'detail']
    list_filter = ['username', 'belong_to', 'brief_introduction', 'detail', 'is_available', 'is_expert']
    list_editable = ['is_available']
    relfield_style = 'fa-ajax'
    show_bookmarks = False
    model_icon = 'glyphicon glyphicon-user'


class RegistrationInfoAdmin(object):
    '''
    Configuration for the label "Registration" in the category "Medical Service".
    '''
    
    list_display = ['id', 'patient', 'doctor', 'appointment_time', 'submission_time', 'status']
    search_fields = ['status']
    list_filter = ['id', 'patient', 'doctor', 'appointment_time', 'submission_time', 'status']
    list_editable = ['status']
    show_bookmarks = False
    refresh_times = (3, 6)
    relfield_style = 'fa-ajax'
    model_icon = 'glyphicon glyphicon-list-alt'
    
    def queryset(self):
        '''
        Control of the registration displayed according to the user permissions.
        '''
        
        registration = super(RegistrationInfoAdmin, self).queryset()
        
        # an administrator can view all the registration
        if self.request.user.is_superuser:
            return registration
        else:
            # a patient can only view his/her registration submitted
            try:
                patient_view = registration.filter(patient = self.request.user.id)
            except AttributeError:
                patient_view = registration.none()
            
            # a doctor can only view his/her patients' registration
            try:
                doctor_info = DoctorInfo.objects.get(username = self.request.user.id)
                doctor_view = registration.filter(doctor = doctor_info.id)
            except ObjectDoesNotExist:
                doctor_view = registration.none()
            
            return doctor_view | patient_view 


# register classes with their managers
xadmin.site.register(HospitalInfo, HospitalInfoAdmin)
xadmin.site.register(DepartmentInfo, DepartmentInfoAdmin)
xadmin.site.register(DoctorInfo, DoctorInfoAdmin)
xadmin.site.register(RegistrationInfo, RegistrationInfoAdmin)