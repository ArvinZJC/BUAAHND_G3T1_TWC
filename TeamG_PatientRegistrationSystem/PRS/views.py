'''
PRS/views.py:
it contains views of the PRS project

created on 16 October, 2018

@author: Liu Haodong, Zhao Jichen, Ye Yifan, and Wang Annong
'''

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from hospitals import models
from users import models as usr
from django.core.exceptions import ObjectDoesNotExist

def home( request ):
    '''
    Show the home page.
    '''
    
    return render( request, 'index.html', context = { 'home_active': 'active' } )

def reg( request ):
    '''
    Show the registration page.
    '''
    
    hs_info = models.HospitalInfo.objects.all()
    dp_info = models.DepartmentInfo.objects.all()
    dr_info = models.DoctorInfo.objects.all()
    return render( request, 'reg.html', context = { 'reg_active': 'active', 'hs_info': hs_info, 'dp_info': dp_info, 'dr_info': dr_info } )

@csrf_exempt
def rec_reg( request ):
    '''
    Show the registration result page.
    '''
    hs = request.POST.get( 'hs' )
    dp = request.POST.get( 'dp' )
    dr = request.POST.get( 'dr' )
    user = request.POST.get( 'user' )
    reg_date = request.POST.get( 'reg_date' )
    dr_username = request.POST.get( 'dr_username' )
    
    if hs != "" and dp != "" and dr != "" and user != "" and reg_date != "":
        try:
            dr_id = usr.UserProfile.objects.get( username = dr_username ).id
            models.RegistrationInfo.objects.create(
                patient = usr.UserProfile.objects.get( username = user ),
                doctor = models.DoctorInfo.objects.get( username = dr_id ),
                appointment_time = reg_date
            )
            return render( request, 'reg_result_success.html' )
        except ObjectDoesNotExist:
            return render( request, 'reg_result_fail.html' )
    else:
        return render( request, 'reg_result_fail.html' )

def data_refresh( request ):
    '''
    Show the registration page with real-time updated data.
    '''
    
    status = str( request.GET.get( 'status' ) )
    
    if status == "hs":
        hs_name = str( request.GET.get( 'ret_data' ) )
        dp_name = models.DepartmentInfo.objects.filter( belong_to__name = hs_name )  #get all the departments of the hospital selected
        counter1 = 1
        context1 = {}
        
        for dp_names in dp_name:
            context1[ str( counter1 ) ] = dp_names.name
            counter1 = counter1 + 1
        
        return JsonResponse( context1 )
    elif status == "dp":
        dp_name = str( request.GET.get( 'ret_data' ) )
        dr_name = models.DoctorInfo.objects.filter( belong_to__name = dp_name )  #get all the doctors of the department and hospital selected
        context2 = {}
        
        for dr_names in dr_name:
            context2[ str( dr_names.username ) ] = str( dr_names )
        
        return JsonResponse( context2 )

def about( request ):
    '''
    Show the system introduction page.
    '''
    
    return render( request, 'about.html', context = { 'about_active': 'active' } )