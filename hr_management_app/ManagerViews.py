from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .decorators import require_user_type
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .decorators import require_user_type
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from .EmployeeViews import employee_apply_leave



@require_user_type(user_type=4)
@login_required(login_url='do_login')
def manager_home(request):
    try:
        employee_apply_leave(request)
        manager_name = request.user.username
        under_employees = CustomUser.objects.filter(manager=manager_name,is_active=True)
        employees_count = Employees.objects.filter(admin__in=under_employees).count()
        return render(request,"hr_management/manager_template/manager_home_template.html",{'employees_count':employees_count})
    except Employees.DoesNotExist:
        return redirect('do_login')    

@require_user_type(user_type=4)
@login_required(login_url='do_login')
def manager_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"hr_management/manager_template/manager_profile.html",{"user":user})


# @require_user_type(user_type=4)
# @login_required(login_url='do_login')
# def manager_profile_save(request):
#     if request.method!="POST":
#         return HttpResponseRedirect(reverse("manager_profile"))
#     else:
#         first_name=request.POST.get("first_name")
#         last_name=request.POST.get("last_name")
#         password=request.POST.get("password")
#         profile_pic=request.POST.get("profile_pic")
#         try:
#             customuser=CustomUser.objects.get(id=request.user.id)
#             customuser.first_name=first_name
#             customuser.last_name=last_name
#             if password!=None and password!="":
#                 customuser.set_password(password)
#             customuser.save()
#             messages.success(request, "Successfully Updated Profile")
#             return HttpResponseRedirect(reverse("manager_home"))
#         except:
#             messages.error(request, "Failed to Update Profile")
#             return HttpResponseRedirect(reverse("manager_home"))

@require_user_type(user_type=4)
@login_required(login_url='do_login')
def manager_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manager_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        
        if 'profile_pic' in request.FILES:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None
        
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            employee = Employees.objects.get(admin=customuser)

            customuser.first_name = first_name
            customuser.last_name = last_name
            if password is not None and password != "":
                customuser.set_password(password)
            customuser.save()

            if profile_pic_url is not None:
                employee.profile_pic = profile_pic_url
                employee.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("manager_home"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("manager_home"))

    


@login_required(login_url='do_login')
@require_user_type(user_type=[1, 4])
def manager_leave_view(request):
    user = request.user
    manager_id = user.id
    manager = CustomUser.objects.get(id=manager_id, user_type='4')
    customusers = CustomUser.objects.filter(manager=manager)
    context = {
        'leaves': [],
        'current_time': datetime.now()
    }
    for customuser in customusers:
        customuser_ids = []
        leave_reports = []
        customuser_ids.append(customuser.id)
        employees = Employees.objects.filter(admin_id__in=customuser_ids)
        for employee in employees:
            l = LeaveReportEmployee.objects.filter(employee_id_id=employee)
            leave_reports.extend(l)
        leave_reports.reverse()
        context['leaves'].extend(leave_reports)
        # Auto-approve pending leave requests for this manager's employees
        for leave in leave_reports:
            if leave.leave_status == 0:
                leave_start_date = datetime.strptime(str(leave.leave_start_date), "%Y-%m-%d").date()
                time_since_request = datetime.now().date() - leave_start_date
                if time_since_request >= timedelta(days=5000):
                    leave.leave_status = 1
                    leave.save()
                    employee_leave = EmployeeLeave.objects.filter(employee_id=leave.employee_id).first()
                    leave_start_date_str = leave.leave_start_date.strftime('%Y-%m-%d')
                    leave_end_date_str = leave.leave_end_date.strftime('%Y-%m-%d')
                    leave_start_date = datetime.strptime(leave_start_date_str, '%Y-%m-%d').date()
                    leave_end_date = datetime.strptime(leave_end_date_str, '%Y-%m-%d').date()
                    num_days = (leave_end_date - leave_start_date).days + 1
                   
                    excluded_days = 0
                        
                    leave_end_date = leave_start_date + timedelta(days=num_days - 1)  # Calculate the end date

                    # Check if leave_end_date is a Saturday or Sunday
                    if leave_end_date.weekday() == 5 or leave_end_date.weekday() == 6:
                        excluded_days += 2  # Exclude both Saturday and Sunday
                    else:
                        excluded_days += 1  # Exclude only Sunday if the end date is a Sunday

                    for i in range(num_days):
                        date = leave_start_date + timedelta(days=i)
                        if date.weekday() == 5 and date != leave_end_date:
                            # Exclude Saturday if it's not the end date
                            excluded_days += 1
                        elif date.weekday() == 6 and date != leave_end_date:
                            # Exclude Sunday if it's not the end date
                            excluded_days += 1
                            
                    if leave.leave_type == 'Earned':
                        employee_leave.EarnLeave_used += num_days
                        if employee_leave.current_EL < num_days:
                            abc = num_days - employee_leave.current_EL
                            employee_leave.current_EL = 0
                            employee_leave.Prev_CFEL = employee_leave.Prev_CFEL - abc
                        else:
                            employee_leave.current_EL = employee_leave.current_EL - num_days
                        employee_leave.EarnLeave = employee_leave.Prev_CFEL + employee_leave.current_EL
                        employee_leave.TotalLeaves = employee_leave.EarnLeave + employee_leave.CasualLeave
                    elif leave.leave_type == 'Casual':
                        total_used_casual_leaves = employee_leave.CasualLeave_used + num_days
                        employee_leave.CasualLeave_used = total_used_casual_leaves
                        employee_leave.CasualLeave = employee_leave.CasualLeave - num_days
                        employee_leave.TotalLeaves = employee_leave.EarnLeave + employee_leave.CasualLeave
                    employee_leave.save()
    if user.user_type == '4':
        return render(request, "hr_management/manager_template/employee_leave_view.html", context)
    else:
        return render(request, "hr_management/admin/employee_leave_view.html", context)


# @login_required(login_url='do_login')
# @require_user_type(user_type=[1, 4])
# def manager_leave_view(request):
#     user = request.user
#     manager_id = user.id
#     manager = CustomUser.objects.get(id=manager_id, user_type='4')
#     customusers = CustomUser.objects.filter(manager=manager)
#     context = {
#         'leaves': [],
#         'current_time': datetime.now()
#     }
#     for customuser in customusers:
#         customuser_ids = []
#         leave_reports = []
#         customuser_ids.append(customuser.id)
#         employees = Employees.objects.filter(admin_id__in=customuser_ids)
#         for employee in employees:
#             l = LeaveReportEmployee.objects.filter(employee_id_id=employee)
#             leave_reports.extend(l)
#         leave_reports.reverse()
#         context['leaves'].extend(leave_reports)
#         # Auto-approve pending leave requests for this manager's employees
#         for leave in leave_reports:
#             if leave.leave_status == 0:
#                 leave_start_date = datetime.strptime(str(leave.leave_start_date), "%Y-%m-%d").date()
#                 time_since_request = datetime.now().date() - leave_start_date
#                 if time_since_request >= timedelta(days=1200):
#                     leave.leave_status = 1
#                     leave.save()
#                     employee_leave = EmployeeLeave.objects.filter(employee_id=leave.employee_id).first()
#                     leave_start_date_str = leave.leave_start_date.strftime('%Y-%m-%d')
#                     leave_end_date_str = leave.leave_end_date.strftime('%Y-%m-%d')
#                     leave_start_date = datetime.strptime(leave_start_date_str, '%Y-%m-%d').date()
#                     leave_end_date = datetime.strptime(leave_end_date_str, '%Y-%m-%d').date()
#                     num_days = (leave_end_date - leave_start_date).days + 1
#                     excluded_days = 0
#                     for i in range(num_days):
#                         date = leave_start_date + timedelta(days=i)
#                         if date.weekday() >= 5:
#                             excluded_days += 1
#                     num_days -= excluded_days
#                     if leave.leave_type == 'Earned':
#                         employee_leave.EarnLeave_used += num_days
#                         if employee_leave.current_EL < num_days:
#                             abc = num_days - employee_leave.current_EL
#                             employee_leave.current_EL = 0
#                             employee_leave.Prev_CFEL = employee_leave.Prev_CFEL - abc
#                         else:
#                             employee_leave.current_EL = employee_leave.current_EL - num_days
#                         employee_leave.EarnLeave = employee_leave.Prev_CFEL + employee_leave.current_EL
#                         employee_leave.TotalLeaves = employee_leave.EarnLeave + employee_leave.CasualLeave
#                     elif leave.leave_type == 'Casual':
#                         total_used_casual_leaves = employee_leave.CasualLeave_used + num_days
#                         employee_leave.CasualLeave_used = total_used_casual_leaves
#                         employee_leave.CasualLeave = employee_leave.CasualLeave - num_days
#                         employee_leave.TotalLeaves = employee_leave.EarnLeave + employee_leave.CasualLeave
#                     employee_leave.save()
#     if user.user_type == '4':
#         return render(request, "hr_management/manager_template/employee_leave_view.html", context)
#     else:
#         return render(request, "hr_management/admin/employee_leave_view.html", context)


      
@login_required(login_url='do_login')
@require_user_type(user_type=[1, 4])
def manageReimbursementView(request):
    try:
        user = request.user
        context = {
            'reimbursements': [],
        }
        if user.user_type == '4':
            manager_id = user.id
            manager = CustomUser.objects.get(id=manager_id, user_type='4')
            customusers = CustomUser.objects.filter(manager=manager)
            for customuser in customusers:
                customuser_ids = [customuser.id]
                employees = Employees.objects.filter(admin_id__in=customuser_ids)
                for employee in employees:
                    reimbursements = Reimbursement_bill.objects.filter(employee_id_id=employee).order_by('-id')
                    context['reimbursements'].extend(reimbursements)
            page = request.GET.get('page')
            paginator = Paginator(context['reimbursements'], 8)
            try:
                context['reimbursements'] = paginator.page(page)
            except PageNotAnInteger:
                context['reimbursements'] = paginator.page(1)
            except EmptyPage:
                context['reimbursements'] = paginator.page(paginator.num_pages)
            except BaseException as a:
                print(a)
            return render(request, "hr_management/manager_template/employee_reimbursement_view.html", context)
        else:
            reimbursements = Reimbursement_bill.objects.all().order_by('-id')
            context['reimbursements'].extend(reimbursements)
            page = request.GET.get('page')
            paginator = Paginator(context['reimbursements'], 10) 
            try:
                context['reimbursements'] = paginator.page(page)
            except PageNotAnInteger:
                context['reimbursements'] = paginator.page(1)
            except EmptyPage:
                context['reimbursements'] = paginator.page(paginator.num_pages)
            return render(request, "hr_management/admin/employee_reimbursement_view.html", context)
    except BaseException as a:
        print(a)