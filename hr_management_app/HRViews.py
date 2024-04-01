from datetime import datetime
from uuid import uuid4
from django.http import Http404
from django.contrib import messages
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from hr_management_app.models import Employees, LeaveReportHR,\
        HRs, FeedBackHRs, CustomUser, NotificationHRs
import logging
logger = logging.getLogger(__name__)
from django.contrib.auth.decorators import login_required
from .views import doLogin
from .decorators import require_user_type


@login_required(login_url=doLogin)
@require_user_type(2)
def hr_home(request):
    employee_count=Employees.objects.all().count()
    hr_count=HRs.objects.all().count()
    manager_count = CustomUser.objects.filter(user_type=4).count()
    account_count = CustomUser.objects.filter(user_type=5).count()
    hrs=HRs.objects.all()

    employee_attendance=Employees.objects.filter()
    employee_list=[]
    for employee in employee_attendance:
        employee_list.append(employee.admin.username)
 
    return render(request,"hr_management/hr/hr_home_template.html",{"employee_count":employee_count,"hr_count":hr_count,"manager_count":manager_count,'account_count':account_count})


@login_required(login_url=doLogin)
@require_user_type(2)
def hr_feedback(request):
    hr_id=HRs.objects.get(admin=request.user.id)
    feedback_data=FeedBackHRs.objects.filter(hr_id=hr_id)
    return render(request,"hr_management/hr/hr_feedback.html",{"feedback_data":feedback_data})


@login_required(login_url=doLogin)
@require_user_type(2)
def hr_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("hr_feedback_save"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        hr_obj=HRs.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackHRs(hr_id=hr_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(("hr_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(("hr_feedback"))


@login_required(login_url=doLogin)
@require_user_type(2)
def hr_profile(request):
    try:
        user=CustomUser.objects.get(id=request.user.id)
        hr=HRs.objects.get(admin=user)
        return render(request,"hr_management/hr/hr_profile.html",{"user":user,"hr":hr})
    except CustomUser.DoesNotExist:
        raise Http404("CustomUser matching query does not exist")
    except HRs.DoesNotExist:
        raise Http404('HR matching query does not exist')


@login_required(login_url=doLogin)
@require_user_type(2)
def hr_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("hr_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        # address=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            hr=HRs.objects.get(admin=customuser.id)
            # hr.address=address
            hr.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("hr_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("hr_profile"))


@login_required(login_url=doLogin)
@require_user_type(2)
@csrf_exempt
def hr_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        hr=HRs.objects.get(admin=request.user.id)
        hr.fcm_token=token
        hr.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


@login_required(login_url=doLogin)
@require_user_type(2)
def hr_all_notification(request):
    hr=HRs.objects.get(admin=request.user.id)
    notifications=NotificationHRs.objects.filter(hr_id=hr.id)
    return render(request,"hr_management/hr/all_notification.html",{"notifications":notifications})


