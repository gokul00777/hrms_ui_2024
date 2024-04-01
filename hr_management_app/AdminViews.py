import json
import requests
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseNotFound
from django.shortcuts import render,render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.conf import settings
from .forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from num2words import num2words
from django.utils.html import strip_tags
from django.db.models import Q
from datetime import datetime,date
from .decorators import require_user_type
from decimal import Decimal
from io import BytesIO
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404,redirect
import weasyprint
from django.db import transaction
import calendar
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import threading
import schedule





@login_required(login_url='do_login')
@require_user_type(1)
def admin_home(request):
    employee_count1=Employees.objects.all().count()
    hr_count=HRs.objects.all().count()
    manager_count = CustomUser.objects.filter(user_type=4).count()
    account_count = CustomUser.objects.filter(user_type=5).count()
    hrs=HRs.objects.all()
    hr_name_list=[]
    for hr in hrs:
        hr_name_list.append(hr.admin.username)

    employees_all=Employees.objects.all()
    employee_name_list=[]
    for employee in employees_all:
        employee_name_list.append(employee.admin.username)
    return render(request,"hr_management/admin/home_content.html",{"employee_count":employee_count1,"hr_count":hr_count,"hr_name_list":hr_name_list,"employee_name_list":employee_name_list,'manager_count':manager_count,'account_count':account_count})


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def add_hr(request):
    manager = CustomUser.objects.filter(user_type=4)
    if request.user.user_type =='2': 
        return render(request,"hr_management/hr/add_hr_template.html")
    else:
        return render(request,"hr_management/admin/add_hr_template.html",{"manager":manager})
      

@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def add_hr_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        department=request.POST.get("department")
        password=request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return HttpResponseRedirect(reverse("add_hr"))
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.hrs.department=department
            user.save()

            # Send email notification
            email_subject = 'HR Account Created'
            application_link = 'http://app1.olatechs.com:8080/'  
            email_template = 'hr_management/admin/hr_account_created.html'  # Path to your email template
            email_context =  {'first_name': first_name, 'last_name': last_name,'email':email,'password':password,'application_link':application_link}  # Context data for the template


            
            # Render the HTML email template and convert it to a plain text version
            email_html_message = render_to_string(email_template, email_context)
            email_plain_message = strip_tags(email_html_message)
            # Set up the email parameters
            from_email = f'{settings.EMAIL_FROM_NAME} <{getattr(settings, "EMAIL_HOST_USER", "default_from_email")}>'
            to_email = email

            # Create the EmailMessage object
            # email_message = EmailMessage(
            #     subject=email_subject,
            #     body=email_plain_message,
            #     from_email=from_email,
            #     to=[to_email]
            # )
            # email_message.send()
            send_mail(email_subject,email_plain_message,from_email,[to_email])

            messages.success(request,"Successfully Added HR")
            return HttpResponseRedirect(reverse("add_hr"))
        except:
            messages.error(request,"Failed to Add HR")
            return HttpResponseRedirect(reverse("add_hr"))


######################################################################################


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def add_account(request):
    account = CustomUser.objects.filter(user_type=5)
    if request.user.user_type =='2': 
        return render(request,"hr_management/hr/add_account_template.html")
    else:
        return render(request,"hr_management/admin/add_account_template.html",{"account":account})
      

@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def add_account_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return HttpResponseRedirect(reverse("add_account"))
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=5)
            user.save()
            # Send email notification
            email_subject = 'Accounts Department Account Created'
            application_link = 'http://app1.olatechs.com:8080/' 
            email_template = 'hr_management/admin/account_account_created.html'  # Path to your email template
            email_context =  {'first_name': first_name, 'last_name': last_name,'email':email,'password':password,'application_link':application_link}  # Context data for the template

            # Render the HTML email template and convert it to a plain text version
            email_html_message = render_to_string(email_template, email_context)
            email_plain_message = strip_tags(email_html_message)
            # Set up the email parameters
            from_email = f'{settings.EMAIL_FROM_NAME} <{getattr(settings, "EMAIL_HOST_USER", "default_from_email")}>'
            to_email = email

            # Create the EmailMessage object
            # email_message = EmailMessage(
            #     subject=email_subject,
            #     body=email_plain_message,
            #     from_email=from_email,
            #     to=[to_email]
            # )
            # email_message.send()
            send_mail(email_subject,email_plain_message,from_email,[to_email])

            messages.success(request,"Successfully Added Account")
            return HttpResponseRedirect(reverse("add_account"))
        except:
            messages.error(request,"Failed to Add Account")
            return HttpResponseRedirect(reverse("add_account"))


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def add_employee(request):
    manager = CustomUser.objects.filter(user_type=4)
    if request.user.user_type =='2': 
        return render(request,"hr_management/hr/add_employee_template.html",{"manager":manager})
    else:
        return render(request,"hr_management/admin/add_employee_template.html",{"manager":manager})
      


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def add_employee_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        manager = request.POST.get("manager")
        department = request.POST.get("department")
        designation = request.POST.get("designation")

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, last_name=last_name, first_name=first_name, manager=manager, user_type=3)
            user.employees.department = department
            user.employees.designation = designation
            user.save()

            # Send email notification
            email_subject = 'Employee Account Created'
            application_link = 'http://app1.olatechs.com:8080/' 
            email_template = 'hr_management/admin/employee_account_created.html'  # Path to your email template
            email_context =  {'first_name': first_name, 'last_name': last_name,'email':email,'password':password,'application_link':application_link}  # Context data for the template

            # Render the HTML email template and convert it to a plain text version
            email_html_message = render_to_string(email_template, email_context)
            email_plain_message = strip_tags(email_html_message)
            # Set up the email parameters
            from_email = f'{settings.EMAIL_FROM_NAME} <{getattr(settings, "EMAIL_HOST_USER", "default_from_email")}>'
            to_email = email

            # Create the EmailMessage object
            send_mail(email_subject,email_plain_message,from_email,[to_email])

            messages.success(request, "Successfully added employee and sent email notification")
            return HttpResponseRedirect(reverse("add_employee"))
        except:
            messages.error(request, "Failed to add employee")
            return HttpResponseRedirect(reverse("add_employee"))
    

@login_required(login_url='do_login')
@require_user_type(user_type=[1, 2])
def manage_hr(request):
    hrs = HRs.objects.all()
    if request.user.user_type == '2':
        return render(request, "hr_management/hr/manage_hr_template.html", {"hrs": hrs})
    else:
        return render(request, "hr_management/admin/manage_hr_template.html", {"hrs": hrs})


# @login_required(login_url='do_login')
# @require_user_type(user_type=[1, 2])
# def manage_employee(request):
#     query = request.GET.get('search')
#     employees = Employees.objects.all()  # Exclude user_type=5

#     if query:
#         employees = employees.filter(
#             Q(admin__email__icontains=query) |
#             Q(admin__first_name__icontains=query) |
#             Q(admin__last_name__icontains=query)
#         )
#         # Check if the query is a number and perform additional filtering
#         if query.isdigit():
#             employees = employees.filter(Q(admin__id=query))

#     if request.user.user_type == '2':
#         return render(request, "hr_management/hr/manage_employee_template.html", {"employees": employees})
#     else:
#         return render(request, "hr_management/admin/manage_employee_template.html", {"employees": employees})


@login_required(login_url='do_login')
@require_user_type(user_type=[1, 2])
def manage_employee(request):
    query = request.GET.get('search')
    employees = Employees.objects.all()

    if query:
        employees = employees.filter(
            Q(admin__email__icontains=query) |
            Q(admin__first_name__icontains=query) |
            Q(admin__last_name__icontains=query)
        )
        if query.isdigit():
            employees = employees.filter(Q(admin__id=query))

    if request.method == 'POST':
        # Get the employee ID from the form
        employee_id = request.POST.get('employee_id')
        is_active = request.POST.get('active_inactive') == 'active'
        # Retrieve the specific employee
        employee = get_object_or_404(Employees, admin__id=employee_id)

        # Update the active status of the specific employee
        employee.admin.is_active = is_active
        employee.admin.save()

    if request.user.user_type == '2':
        return render(request, "hr_management/hr/manage_employee_template.html", {"employees": employees})
    else:
        return render(request, "hr_management/admin/manage_employee_template.html", {"employees": employees})



@login_required(login_url='do_login')
@require_user_type(user_type=[1, 2])
def manage_account_section(request):
    query = request.GET.get('search')
    accounts = CustomUser.objects.filter(user_type=5)
    if query:
        accounts = accounts.filter(
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |  # Use icontains for case-insensitive matching
            Q(last_name__icontains=query)
        )

        if query.isdigit():
            accounts = accounts.filter(Q(id=query))
    if request.user.user_type == '2':
        return render(request, "hr_management/hr/manage_accountant_template.html", {"accounts": accounts})
    else:
        return render(request, "hr_management/admin/manage_accountant_template.html", {"accounts": accounts})




@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def add_manager(request):
    try:
        manager = CustomUser.objects.filter(Q(user_type=4) | Q(user_type=1))
        if request.user.user_type =='2': 
            return render(request,"hr_management/hr/add_manager_template.html",{"manager":manager})
        else:
            return render(request,"hr_management/admin/add_manager_template.html",{"manager":manager})
    except:
        messages.error(request,"Failed to Add Manager")
        return HttpResponseRedirect(reverse("add_manager"))



@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def add_manager_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        manager=request.POST.get("manager")
        department=request.POST.get("department")
        designation=request.POST.get("designation")

        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,manager=manager,user_type=4)
            user.employees.department=department
            user.employees.designation=designation
            user.save()
            
            # Send email notification
            email_subject = 'Manager Account Created'
            application_link = 'http://app1.olatechs.com:8080/' 
            email_template = 'hr_management/admin/manager_account_created.html'  # Path to your email template
            email_context =  {'first_name': first_name, 'last_name': last_name,'email':email,'password':password,'application_link':application_link}  # Context data for the template

            # Render the HTML email template and convert it to a plain text version
            email_html_message = render_to_string(email_template, email_context)
            email_plain_message = strip_tags(email_html_message)
            # Set up the email parameters
            from_email = f'{settings.EMAIL_FROM_NAME} <{getattr(settings, "EMAIL_HOST_USER", "default_from_email")}>'
            to_email = email
            send_mail(email_subject,email_plain_message,from_email,[to_email])

            messages.success(request,"Successfully Added Manager")
            return HttpResponseRedirect(reverse("add_manager"))
        except:
            messages.error(request,"Failed to Add Manager")
            return HttpResponseRedirect(reverse("add_manager"))



@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def edit_hr(request,hr_id):
    manager = CustomUser.objects.filter(user_type=4)
    hr=HRs.objects.get(admin=hr_id)
    if request.user.user_type=='1':
        return render(request,"hr_management/admin/edit_hr_template.html",{"hr":hr,"id":hr_id,'manager':manager})
    else:
        return render(request,"hr_management/hr/edit_hr_template.html",{"hr":hr,"id":hr_id,'manager':manager})


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def edit_hr_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        hr_id=request.POST.get("hr_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")
        manager= request.POST.get('manager')
        department= request.POST.get('department')

        

        try:
            user=CustomUser.objects.get(id=hr_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.manager = manager
            user.save()

            hr_model=HRs.objects.get(admin=hr_id)
            hr_model.address=address
            hr_model.manager=manager
            hr_model.department=department
            hr_model.save()
            messages.success(request,"Successfully Edited Staf HR")
            return redirect('manage_hr')
        except:
            messages.error(request,"Failed to Edit HR")




@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def edit_employee(request,employee_id):
    manager = CustomUser.objects.filter(user_type=4)
    employee=Employees.objects.get(admin=employee_id)
    if request.user.user_type == '2':
        return render(request,"hr_management/hr/edit_employee_template.html",{"employee":employee,"id":employee_id,'manager':manager})
    else:
        return render(request,"hr_management/admin/edit_employee_template.html",{"employee":employee,"id":employee_id,'manager':manager})


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def edit_employee_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        employee_id=request.POST.get("employee_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        manager= request.POST.get('manager')
        designation = request.POST.get("designation")
        department = request.POST.get("department")

        try:
            user=CustomUser.objects.get(id=employee_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.manager = manager
            user.save()
            employee_model=Employees.objects.get(admin=employee_id)
            employee_model.designation=designation
            employee_model.department=department
            employee_model.save()
            messages.success(request,"Successfully Edited Employee")
            return redirect('manage_employee')
        except:
            messages.error(request,"Failed to Edit Manager")




@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def edit_account_section(request,employee_id):
    try:
        customuser = CustomUser.objects.filter(user_type=5)
        account=Accounts.objects.get(admin_id=employee_id)
        if request.user.user_type == '2':
            return render(request,"hr_management/hr/edit_account_template.html",{"id":employee_id,'account':account,'customuser':customuser})
        else:
            return render(request,"hr_management/admin/edit_account_template.html",{"id":employee_id,'account':account,'customuser':customuser})

    except:
        messages.error(request,"Account Not Found")

@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def edit_account_section_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        employee_id=request.POST.get("employee_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        try:
            user=CustomUser.objects.get(id=employee_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()
            messages.success(request,"Successfully Edited Account")
            return redirect('manage_account_section')
        except:
            messages.error(request,"Failed to Edit Account")


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def delete_account_section(request, employee_id):
    user = CustomUser.objects.get(id=employee_id)
    context ={'user':user}
    if request.method == 'POST':
         user.delete()
         messages.success(request, "Account Deleted Successfully")
         return HttpResponseRedirect(reverse('manage_account_section'))
    if request.user.user_type == '2':
        return render(request,'hr_management/hr/delete_account_template.html',context)
    else:
        return render(request,'hr_management/admin/delete_account_template.html',context)



@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def delete_employee(request, employee_id):
    user = CustomUser.objects.get(id=employee_id)
    context ={'user':user}
    if request.method == 'POST':
         user.delete()
         messages.success(request, "Employee Deleted Successfully")
         return HttpResponseRedirect(reverse('manage_employee'))
    if request.user.user_type == '2':
        return render(request,'hr_management/hr/delete_employee_template.html',context)
    else:
        return render(request,'hr_management/admin/delete_employee_template.html',context)


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def delete_hr(request, hr_id):
    try:
        user = CustomUser.objects.get(id=hr_id)
        context ={'user':user}
        if request.method == 'POST':
            user.delete()
            messages.success(request, "HR Deleted Successfully")
            return HttpResponseRedirect(reverse('manage_hr'))
        if request.user.user_type == '1':
            return render(request,'hr_management/admin/delete_hr_template.html',context)
        else:
            return render(request,'hr_management/hr/delete_hr_template.html',context)
    except:
        messages.error(request, 'HR Not Available')
        
        


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def employee_details(request, employee_id):
    try:
        user = CustomUser.objects.get(id=employee_id)
        employee=Employees.objects.get(admin=user)
        personal_info = Employee_Onboarding.objects.filter(employee=employee)
        current_address = Address_detail.objects.filter(employee=employee)
        per_address = Permanent_Address.objects.filter(employee=employee)
        emp_family_details = FamilyDetails.objects.filter(employee=employee)
        bank_details =BankDetails.objects.filter(employee=employee)
        documents = Documents.objects.filter(employee=employee)
        
    except CustomUser.DoesNotExist:
        messages.error(request, 'Employee Not Available')
    
    context = {'user':user,'personal_info': personal_info, 'current_address': current_address, 'per_address':per_address,'emp_family_details':emp_family_details,'bank_details':bank_details,'documents': documents,'employee':employee} 
    if request.user.user_type == '2':
        return render(request, 'hr_management/hr/employee_onboarding_details.html', context)
    else:
        return render(request, 'hr_management/admin/employee_onboarding_details.html', context)


#################################### delete onboarding details #######################
@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def employee_details_delete(request, employee_id):
    try:
        user = CustomUser.objects.get(id=employee_id)
        employee = Employees.objects.get(admin=user)
        personal_info = Employee_Onboarding.objects.get(employee_id=employee)
        current_address = Address_detail.objects.get(employee_id=employee)
        per_address = Permanent_Address.objects.get(employee_id=employee)
        emp_family_details = FamilyDetails.objects.get(employee_id=employee)
        bank_details = BankDetails.objects.get(employee_id=employee)
        documents = Documents.objects.get(employee_id=employee)
        leave = EmployeeLeave.objects.get(employee_id=employee)
        personal_info.delete()
        current_address.delete()
        per_address.delete()
        emp_family_details.delete()
        bank_details.delete()
        documents.delete()
        leave.delete()
        return redirect('employee_details',user.id)
    except:
        return HttpResponse("An error occurred while deleting employee details.")

############################################ edit onboarding details #######################

@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def edit_employee_onboarding(request, employee_id):
    try:
        user = CustomUser.objects.get(id=employee_id)
        employee = Employees.objects.get(admin=user)
        personal_info = Employee_Onboarding.objects.get(employee=employee)
        current_address = Address_detail.objects.get(employee=employee)
        per_address = Permanent_Address.objects.get(employee=employee)
        emp_family_details = FamilyDetails.objects.get(employee=employee)
        bank_details = BankDetails.objects.get(employee=employee)
        documents = Documents.objects.get(employee=employee)

        if request.method == 'POST':
            new_emp_id = request.POST.get('emp_id')
            employee.emp_id = new_emp_id
            employee.save()
            emp_onboarding_form = EmployeeOnboardingForm(request.POST, instance=personal_info)
            emp_address_form = EmployeeAddressDetailsFrom(request.POST, instance=current_address)
            emp_perment_address_form = EmployeePermentAddressFrom(request.POST, instance=per_address)
            emp_family_form = FamilyDetailsForm(request.POST, instance=emp_family_details)
            emp_bank_form = BankDetailsForm(request.POST, instance=bank_details)
            emp_document_form = DocumentsForm(request.POST, instance=documents)

            if (
                emp_onboarding_form.is_valid() and
                emp_address_form.is_valid() and
                emp_perment_address_form.is_valid() and
                emp_family_form.is_valid() and
                emp_bank_form.is_valid() and
                emp_document_form.is_valid()
            ):
                emp_onboarding_form.save()
                emp_address_form.save()
                emp_perment_address_form.save()
                emp_family_form.save()
                emp_bank_form.save()
                emp_document_form.save()
                
                return redirect('employee_details', employee_id=employee_id)
        else:
            emp_onboarding_form = EmployeeOnboardingForm(instance=personal_info)
            emp_address_form = EmployeeAddressDetailsFrom(instance=current_address)
            emp_perment_address_form = EmployeePermentAddressFrom(instance=per_address)
            emp_family_form = FamilyDetailsForm(instance=emp_family_details)
            emp_bank_form = BankDetailsForm(instance=bank_details)
            emp_document_form = DocumentsForm(instance=documents)

        context = {
            'user': user,
            'employee': employee,
            'emp_onboarding_form': emp_onboarding_form,
            'emp_address_form': emp_address_form,
            'emp_perment_address_form': emp_perment_address_form,
            'emp_family_form': emp_family_form,
            'emp_bank_form': emp_bank_form,
            'emp_document_form': emp_document_form,
        }

        if request.user.user_type == '1':
            return render(request, 'hr_management/admin/employee_onboarding.html', context)
        else:
            return render(request, 'hr_management/hr/employee_onboarding.html', context)
    except :
        messages.success(request, "Failed to edit onboarding data")
    return redirect('employee_details', employee_id=employee_id)

@login_required(login_url='do_login')
@require_user_type(user_type=[1,4])
def employee_leave_view(request):
    leaves = LeaveReportEmployee.objects.all()
    # Approve pending leave requests that have been pending for more than 7 days
    for leave in leaves:
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
                        print("employee_leave.current_EL222222",employee_leave.current_EL)
                    employee_leave.EarnLeave = employee_leave.Prev_CFEL + employee_leave.current_EL
                    employee_leave.TotalLeaves = employee_leave.EarnLeave + employee_leave.CasualLeave
                elif leave.leave_type == 'Casual':
                    total_used_casual_leaves = employee_leave.CasualLeave_used + num_days
                    employee_leave.CasualLeave_used = total_used_casual_leaves
                    employee_leave.CasualLeave = employee_leave.CasualLeave - num_days
                    employee_leave.TotalLeaves = employee_leave.EarnLeave + employee_leave.CasualLeave
                employee_leave.save()
    leaves = LeaveReportEmployee.objects.order_by('-id').all()
    if request.user.user_type == '4':
        return render(request, "hr_management/manager_template/employee_leave_view.html", {"leaves": leaves, "current_time": datetime.now()})
    else:
        return render(request, "hr_management/admin/employee_leave_view.html", {"leaves": leaves, "current_time": datetime.now()})

# @login_required(login_url='do_login')
# @require_user_type(user_type=[1,4])
# def employee_leave_view(request):
#     leaves = LeaveReportEmployee.objects.all()
#     # Approve pending leave requests that have been pending for more than 7 days
#     for leave in leaves:
#         if leave.leave_status == 0:
#             leave_start_date = datetime.strptime(str(leave.leave_start_date), "%Y-%m-%d").date()
#             time_since_request = datetime.now().date() - leave_start_date
#             if time_since_request >= timedelta(days=1500):
#                 leave.leave_status = 1
#                 leave.save()
#                 employee_leave = EmployeeLeave.objects.filter(employee_id=leave.employee_id).first()
#                 leave_start_date_str = leave.leave_start_date.strftime('%Y-%m-%d')
#                 leave_end_date_str = leave.leave_end_date.strftime('%Y-%m-%d')
#                 leave_start_date = datetime.strptime(leave_start_date_str, '%Y-%m-%d').date()
#                 leave_end_date = datetime.strptime(leave_end_date_str, '%Y-%m-%d').date()
#                 num_days = (leave_end_date - leave_start_date).days + 1
#                 excluded_days = 0
#                 for i in range(num_days):
#                     date = leave.leave_start_date + timedelta(days=i)
#                     if date.weekday() >= 5:
#                         excluded_days += 1
#                 num_days -= excluded_days
#                 if leave.leave_type == 'Earned':
#                     employee_leave.EarnLeave_used += num_days
#                     if employee_leave.current_EL < num_days:
#                         abc = num_days - employee_leave.current_EL
#                         employee_leave.current_EL = 0
#                         employee_leave.Prev_CFEL = employee_leave.Prev_CFEL - abc
#                     else:
#                         employee_leave.current_EL = employee_leave.current_EL - num_days
#                     employee_leave.EarnLeave = employee_leave.Prev_CFEL + employee_leave.current_EL
#                     employee_leave.TotalLeaves = employee_leave.EarnLeave + employee_leave.CasualLeave
#                 elif leave.leave_type == 'Casual':
#                     total_used_casual_leaves = employee_leave.CasualLeave_used + num_days
#                     employee_leave.CasualLeave_used = total_used_casual_leaves
#                     employee_leave.CasualLeave = employee_leave.CasualLeave - num_days
#                     employee_leave.TotalLeaves = employee_leave.EarnLeave + employee_leave.CasualLeave
#                 employee_leave.save()
#     # leaves = LeaveReportEmployee.objects.all()
#     leaves = LeaveReportEmployee.objects.order_by('-id').all()
#     if request.user.user_type == '4':
#         return render(request, "hr_management/manager_template/employee_leave_view.html", {"leaves": leaves, "current_time": datetime.now()})
#     else:
#         return render(request, "hr_management/admin/employee_leave_view.html", {"leaves": leaves, "current_time": datetime.now()})


@login_required(login_url='do_login')
@require_user_type(1)
def manage_session(request):
    return render(request,"hr_management/admin/manage_session_template.html")

@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
@csrf_exempt
def check_mobile_number_exist(request):
    mobile_no=request.POST.get("mobile_no")
    user_obj=OfferLetter_Sended.objects.filter(mobile_no=mobile_no).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
    

@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@login_required(login_url='do_login')
@require_user_type(1)
def hr_feedback_message(request):
    feedbacks=FeedBackHRs.objects.all()
    return render(request,"hr_management/admin/hr_feedback_template.html",{"feedbacks":feedbacks})


@login_required(login_url='do_login')
@require_user_type(1)
def employee_feedback_message(request):
    feedbacks=FeedBackEmployee.objects.all()
    return render(request,"hr_management/admin/employee_feedback_template.html",{"feedbacks":feedbacks})

@login_required(login_url='do_login')
@require_user_type(1)
@csrf_exempt
def employee_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackEmployee.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


@login_required(login_url='do_login')
@require_user_type(1)
@csrf_exempt
def hr_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackHRs.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def hr_leave_view(request):
    leaves=LeaveReportHR.objects.all()
    if request.user.user_type == '2':
        return render(request,"hr_management/hr/hr_leave_view.html",{"leaves":leaves})
    else:
        return render(request,"hr_management/admin/hr_leave_view.html",{"leaves":leaves})


@login_required(login_url='do_login')
@require_user_type(user_type=[1,4])
def employee_approve_leave(request, leave_id):
    leave = LeaveReportEmployee.objects.filter(id=leave_id).first()
    current_date = datetime.now().date()
      
    emp_id = leave.employee_id
    leave.leave_status = 1
    leave.save()
    first_name = emp_id.admin.first_name
    last_name = emp_id.admin.last_name
    employee_leave = EmployeeLeave.objects.filter(employee_id=emp_id).first()
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
            excluded_days += 1
        elif date.weekday() == 6 and date != leave_end_date:
            excluded_days += 1

   
    if leave.leave_type == 'Earned':
        if leave_start_date.year < current_date.year:
            employee_leave.Prev_CFEL -= num_days

        else:
            employee_leave.EarnLeave_used += num_days
            if employee_leave.current_EL < num_days:
                abc = num_days - employee_leave.current_EL
                employee_leave.current_EL = 0
               
                employee_leave.Prev_CFEL = employee_leave.Prev_CFEL - abc
                
            else:
                employee_leave.current_EL = employee_leave.current_EL - num_days
        employee_leave.EarnLeave = employee_leave.Prev_CFEL + employee_leave.current_EL
        employee_leave.TotalLeaves = employee_leave.EarnLeave + employee_leave.CasualLeave
        employee_leave.save()
    elif leave.leave_type == 'Casual':
        total_Used_casual_leaves = employee_leave.CasualLeave_used + num_days
        employee_leave.CasualLeave_used = total_Used_casual_leaves
        employee_leave.CasualLeave = employee_leave.CasualLeave - num_days
        employee_leave.TotalLeaves = employee_leave.EarnLeave + employee_leave.CasualLeave
        employee_leave.save()
    email_subject = 'Leave Request Approved'
    email_template = 'hr_management/admin/leave_request_approved.html'  # Path to your email template
    email_context = {'employee': employee_leave,'first_name':first_name,'last_name':last_name,'leave_start_date':leave_start_date,'leave_end_date':leave_end_date}  # Context data for the template
    # Render the HTML email template and convert it to a plain text version
    email_html_message = render_to_string(email_template, email_context)
    email_plain_message = strip_tags(email_html_message)
    # Set up the email parameters
    from_email = f'{settings.EMAIL_FROM_NAME} <{getattr(settings, "EMAIL_HOST_USER", "default_from_email")}>'
    to_email = emp_id.admin.email
    send_mail(email_subject, email_plain_message, from_email, [to_email])
    if request.user.user_type == '1':
        return HttpResponseRedirect(reverse("employee_leave_view"))
    else:
        return HttpResponseRedirect(reverse("manager_leave_view"))


# def employee_approve_leave(request, leave_id):
#     leave = LeaveReportEmployee.objects.filter(id=leave_id).first()
#     emp_id = leave.employee_id
#     leave.leave_status = 1
#     leave.save()
#     first_name = emp_id.admin.first_name
#     last_name = emp_id.admin.last_name
#     employee_leave = EmployeeLeave.objects.filter(employee_id=emp_id).first()
#     leave_start_date_str = leave.leave_start_date.strftime('%Y-%m-%d')
#     leave_end_date_str = leave.leave_end_date.strftime('%Y-%m-%d')
#     leave_start_date = datetime.strptime(leave_start_date_str, '%Y-%m-%d').date()
#     leave_end_date = datetime.strptime(leave_end_date_str, '%Y-%m-%d').date()
#     num_days = (leave_end_date - leave_start_date).days + 1
    
#     excluded_days = 0
          
#     leave_end_date = leave_start_date + timedelta(days=num_days - 1)  # Calculate the end date

#     # Check if leave_end_date is a Saturday or Sunday
#     if leave_end_date.weekday() == 5 or leave_end_date.weekday() == 6:
#         excluded_days += 2  # Exclude both Saturday and Sunday
#     else:
#         excluded_days += 1  # Exclude only Sunday if the end date is a Sunday

#     for i in range(num_days):
#         date = leave_start_date + timedelta(days=i)
#         if date.weekday() == 5 and date != leave_end_date:
#             excluded_days += 1
#         elif date.weekday() == 6 and date != leave_end_date:
#             excluded_days += 1

   
#     if leave.leave_type == 'Earned':
#         if leave_start_date < datetime(2022, 12, 31).date():
#            pass
#         else:
#             employee_leave.EarnLeave_used += num_days
#             if employee_leave.current_EL < num_days:
#                 abc = num_days - employee_leave.current_EL
#                 employee_leave.current_EL = 0
               
#                 employee_leave.Prev_CFEL = employee_leave.Prev_CFEL - abc
                
#             else:
#                 employee_leave.current_EL = employee_leave.current_EL - num_days
#         employee_leave.EarnLeave = employee_leave.Prev_CFEL + employee_leave.current_EL
#         employee_leave.TotalLeaves = employee_leave.EarnLeave + employee_leave.CasualLeave
#         employee_leave.save()
#     elif leave.leave_type == 'Casual':
#         total_Used_casual_leaves = employee_leave.CasualLeave_used + num_days
#         employee_leave.CasualLeave_used = total_Used_casual_leaves
#         employee_leave.CasualLeave = employee_leave.CasualLeave - num_days
#         employee_leave.TotalLeaves = employee_leave.EarnLeave + employee_leave.CasualLeave
#         employee_leave.save()
#     email_subject = 'Leave Request Approved'
#     email_template = 'hr_management/admin/leave_request_approved.html'  # Path to your email template
#     email_context = {'employee': employee_leave,'first_name':first_name,'last_name':last_name,'leave_start_date':leave_start_date,'leave_end_date':leave_end_date}  # Context data for the template
#     # Render the HTML email template and convert it to a plain text version
#     email_html_message = render_to_string(email_template, email_context)
#     email_plain_message = strip_tags(email_html_message)
#     # Set up the email parameters
#     from_email = f'{settings.EMAIL_FROM_NAME} <{getattr(settings, "EMAIL_HOST_USER", "default_from_email")}>'
#     to_email = emp_id.admin.email
#     send_mail(email_subject, email_plain_message, from_email, [to_email])
#     if request.user.user_type == '1':
#         return HttpResponseRedirect(reverse("employee_leave_view"))
#     else:
#         return HttpResponseRedirect(reverse("manager_leave_view"))


@login_required(login_url='do_login')
@require_user_type(user_type=[1,4])
def employee_disapprove_leave(request, leave_id):
    leave = LeaveReportEmployee.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()        

    # Get the associated CustomUser instance
    employee = leave.employee_id
    first_name = employee.admin.first_name
    last_name = employee.admin.last_name
    
    # Send email notification
    email_subject = 'Leave Request Disapproved'
    email_template = 'hr_management/admin/leave_request_disapproved.html'  # Path to your email template
    email_context = {'employee': employee, 'first_name': first_name, 'last_name': last_name}  # Context data for the template

    # Render the HTML email template and convert it to a plain text version
    email_html_message = render_to_string(email_template, email_context)
    email_plain_message = strip_tags(email_html_message)

    # Set up the email parameters
    from_email = f'{settings.EMAIL_FROM_NAME} <{getattr(settings, "EMAIL_HOST_USER", "default_from_email")}>'
    to_email = employee.admin.email
    send_mail(email_subject,email_plain_message,from_email,[to_email])

    if request.user.user_type == '1':
        return HttpResponseRedirect(reverse("employee_leave_view"))
    else:
        return HttpResponseRedirect(reverse("manager_leave_view"))
        


@login_required(login_url='do_login')
@require_user_type(1)
def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"hr_management/admin/admin_profile.html",{"user":user})


@login_required(login_url='do_login')
@require_user_type(1)
def admin_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_home"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_home"))



@login_required(login_url='do_login')
@require_user_type(1)
@csrf_exempt
def admin_send_notification_employee(request):
    employees=Employees.objects.all()
    return render(request,"hr_management/admin/employee_notification.html",{"employees":employees})



@login_required(login_url='do_login')
@require_user_type(1)
def admin_send_notification_hr(request):
    hrs=HRs.objects.all()
    return render(request,"hr_management/admin/hr_notification.html",{"hrs":hrs})



@login_required(login_url='do_login')
@require_user_type(1)
@csrf_exempt
def send_employee_notification(request):
    id=request.POST.get("id")
    message=request.POST.get("message")
    employee=Employees.objects.get(admin=id)
    token=employee.fcm_token
    url="https://fcm.googleapis.com/fcm/send"
    body={
        "notification":{
            "title":"HR Management System",
            "body":message,
            "click_action": "https://hrmanagementsystem22.herokuapp.com/employee_all_notification",
            "icon": "http://hrmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=NotificationEmployee(employee_id=employee,message=message)
    notification.save()
    return HttpResponse("True")



@login_required(login_url='do_login')
@require_user_type(1)
@csrf_exempt
def send_hr_notification(request):
    id=request.POST.get("id")
    message=request.POST.get("message")
    hr=HRs.objects.get(admin=id)
    token=hr.fcm_token
    url="https://fcm.googleapis.com/fcm/send"
    body={
        "notification":{
            "title":"HR Management System",
            "body":message,
            "click_action":"https://hrmanagementsystem22.herokuapp.com/hr_all_notification",
            "icon":"http://hrmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=NotificationHRs(hr_id=hr,message=message)
    notification.save()
    return HttpResponse("True")

###################################### TO GENERATE PDF ###################################


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def generate_offer_letter(request):
    try:
        if request.method == 'POST':
            offer_letter_sended = OfferLetter_Sended()
            offer_letter_sended.ctc = float(request.POST.get('ctc'))
            offer_letter_sended.name = request.POST.get('name')
            offer_letter_sended.email = request.POST.get('email')
            offer_letter_sended.offer_release_date = request.POST.get('offer_release_date')
            offer_letter_sended.joining_date = request.POST.get('joining_date')
            offer_letter_sended.reporting = request.POST.get('reporting')
            offer_letter_sended.address = request.POST.get('address')
            offer_letter_sended.designation = request.POST.get('designation')
            offer_letter_sended.department = request.POST.get('department')
            offer_letter_sended.job_grade = request.POST.get('job_grade')
            offer_letter_sended.hr_name = request.POST.get('hr_name')
            offer_letter_sended.offer_accept_date = request.POST.get('offer_accept_date')
            offer_letter_sended.mobile_no = request.POST.get('mobile_no')
            formatted_date = datetime.strptime(offer_letter_sended.offer_release_date, '%Y-%m-%d').strftime('%d%m%Y')
            name = request.POST.get('name')
            offer_release_date = request.POST.get('offer_release_date')
            date_object = datetime.strptime(offer_release_date, '%Y-%m-%d')
            offer_release_date = date_object.strftime('%d - %b - %Y')
            amount = offer_letter_sended.ctc
            amount_words = num2words(amount, lang='en_IN', to='currency', currency='INR')
            amount_words = amount_words.replace('Indian Rupees', '').replace('zero paise', '').replace(',', '') 
            joining_date = request.POST.get('joining_date')
            date_object = datetime.strptime(joining_date, '%Y-%m-%d')
            joining_date = date_object.strftime('%d - %b - %Y')
            time = request.POST.get('time')
            address = request.POST.get('address')
            designation = request.POST.get('designation')
            department = request.POST.get('department')
            gender = request.POST.get('gender')
            job_grade = request.POST.get('job_grade')
            reporting = request.POST.get('reporting')
            hr_name = request.POST.get('hr_name')
            offer_accept_date = request.POST.get('offer_accept_date')
            date_object = datetime.strptime(offer_accept_date, '%Y-%m-%d')
            offer_accept_date = date_object.strftime('%d - %b - %Y')
            ctc = offer_letter_sended.ctc
            if ctc <=  273700:
                esic = 0.0325 * ctc
                insurance_premiums = 0
            else:
                esic = 0
                insurance_premiums = 11000.0
            total_variable_pay = ctc * 0.10
            total_fixed_pay = ctc - total_variable_pay - insurance_premiums
            basic_pay = total_fixed_pay * 0.40
            employer_pf_contribution = 0.13 * basic_pay
            hra = 0.50 * basic_pay
            if ctc <=  273700:
                flexible_components_tfp = total_fixed_pay - basic_pay - hra - employer_pf_contribution - esic
            else:
                flexible_components_tfp = total_fixed_pay - basic_pay - hra - employer_pf_contribution
            total_cost_to_company = total_fixed_pay + total_variable_pay + insurance_premiums
            with transaction.atomic():
                offer_letter = OfferLetter(
                    basic_pay=basic_pay,
                    hra=hra,
                    total_fixed_pay=total_fixed_pay,
                    total_variable_pay=total_variable_pay,
                    insurance_premiums=insurance_premiums,
                    total_cost_to_company=total_cost_to_company,
                    employer_pf_contribution=employer_pf_contribution,
                    flexible_components_tfp=flexible_components_tfp,
                    esic = esic
                )
                offer_letter.save()
                offer_letter_sended.offerletter_id = offer_letter.id
                offer_letter_id = offer_letter_sended.offerletter_id
                offer_letter_sended.save()
                if request.user.user_type == '1':
                # Render offer letter HTML template
                    offer_letter_html = render_to_string('hr_management/admin/offer_letter.html', {'offer_letter': offer_letter, \
                                                        'name': name, 'amount_words': amount_words,'joining_date':joining_date,\
                                                        'reporting':reporting, 'time':time,'address':address,'offer_release_date':offer_release_date,\
                                                        'designation':designation,'job_grade':job_grade,'offer_letter_id':offer_letter_id,'hr_name':hr_name,\
                                                        'offer_accept_date':offer_accept_date, 'formatted_date':formatted_date, 'esic':esic,'gender':gender,'department':department}, request=request)
                    # Create a PDF file from HTML template
                    pdf_file = BytesIO()
                    weasyprint.HTML(string=offer_letter_html, base_url=request.build_absolute_uri()).write_pdf(pdf_file)
                    # Create and return the PDF response
                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="offer_letter.pdf"'
                    response.write(pdf_file.getvalue())
                    return response
                else:
                    offer_letter_html = render_to_string('hr_management/hr/offer_letter.html', {'offer_letter': offer_letter, \
                                                        'name': name, 'amount_words': amount_words,'joining_date':joining_date,\
                                                        'reporting':reporting, 'time':time,'address':address,'offer_release_date':offer_release_date,\
                                                        'designation':designation,'job_grade':job_grade,'offer_letter_id':offer_letter_id,'hr_name':hr_name,\
                                                        'offer_accept_date':offer_accept_date, 'formatted_date':formatted_date, 'esic':esic}, request=request)
                    # Create a PDF file from HTML template
                    pdf_file = BytesIO()
                    weasyprint.HTML(string=offer_letter_html, base_url=request.build_absolute_uri()).write_pdf(pdf_file)
                    # Create and return the PDF response
                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="offer_letter.pdf"'
                    response.write(pdf_file.getvalue())
                    return response
        if request.user.user_type == '1':
            return render(request, 'hr_management/admin/generate_offer_letter.html')
        else:
            return render(request, 'hr_management/hr/generate_offer_letter.html')
    except:
        messages.error(request,"Please put requited details")
        return HttpResponseRedirect(reverse("generate_offer_letter"))



###############################################All Offer Letter Sended Record #######################################
@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def offer_letter_sended_history(request):
    offer_letters_sended = OfferLetter_Sended.objects.all()
    paginator = Paginator(offer_letters_sended, 10)  # 10 items per page
    page = request.GET.get('page')
    offer_letters_sended = paginator.get_page(page)
    if request.user.user_type == '1':
        return render(request, 'hr_management/admin/offer_letter_sended_history.html', {'offer_letters_sended': offer_letters_sended})
    else:
        return render(request, 'hr_management/hr/offer_letter_sended_history.html', {'offer_letters_sended': offer_letters_sended})




########################################## Download Offerletter #############################################
@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def download_offer_letter(request, offer_letter_id):
    offer_letter_sended = get_object_or_404(OfferLetter_Sended, offerletter_id=offer_letter_id)
    offer_letter = get_object_or_404(OfferLetter, id=offer_letter_id)
    name = offer_letter_sended.name
    email = offer_letter_sended.email
    offer_release_date = offer_letter_sended.offer_release_date
    joining_date = offer_letter_sended.joining_date
    designation =offer_letter_sended. designation
    department = offer_letter_sended.department
    reporting = offer_letter_sended.reporting
    address = offer_letter_sended.address
    job_grade = offer_letter_sended.job_grade
    hr_name = offer_letter_sended.hr_name
    offer_accept_date = offer_letter_sended.offer_accept_date
    mobile_no = offer_letter_sended.mobile_no
    formatted_date = offer_letter_sended.offer_release_date.strftime('%d%m%Y')
    offer_letter_id = offer_letter_sended.offerletter_id
    formatted_date = formatted_date
    offer_letter_html = render_to_string('hr_management/admin/offer_letter.html', {
        'offer_letter': offer_letter,
        'offer_letter_sended': offer_letter_sended,
        'name': name,
        'email':email,
        'offer_release_date':offer_release_date,
        'joining_date':joining_date,
        'designation':designation,
        'department':department,
        'reporting':reporting,
        'address':address,
        'job_grade':job_grade,
        'hr_name':hr_name,
        'offer_accept_date':offer_accept_date,
        'mobile_no':mobile_no,
        'formatted_date':formatted_date,
        'offer_letter_id':offer_letter_id
    })
    pdf_file = BytesIO()
    weasyprint.HTML(string=offer_letter_html, base_url=request.build_absolute_uri()).write_pdf(pdf_file)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="offer_letter_{offer_letter_id}.pdf"'
    response.write(pdf_file.getvalue())
    return response
#################################################### view offerletter#########################################
@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def view_offer_letter(request, offer_letter_id):
    offer_letter_sended = get_object_or_404(OfferLetter_Sended, offerletter_id=offer_letter_id)
    offer_letter = get_object_or_404(OfferLetter, id=offer_letter_id)
    name = offer_letter_sended.name
    email = offer_letter_sended.email
    offer_release_date = offer_letter_sended.offer_release_date
    joining_date = offer_letter_sended.joining_date
    designation = offer_letter_sended.designation
    department = offer_letter_sended.department
    reporting = offer_letter_sended.reporting
    address = offer_letter_sended.address
    job_grade = offer_letter_sended.job_grade
    hr_name = offer_letter_sended.hr_name
    offer_accept_date = offer_letter_sended.offer_accept_date
    mobile_no = offer_letter_sended.mobile_no
    formatted_date = offer_letter_sended.offer_release_date.strftime('%d%m%Y')
    formatted_date = formatted_date
    offer_letter_id = offer_letter_sended.offerletter_id
    return render(request, 'hr_management/admin/offer_letter.html', {
        'offer_letter': offer_letter,
        'offer_letter_sended': offer_letter_sended,
        'name': name,
        'email': email,
        'offer_release_date': offer_release_date,
        'joining_date': joining_date,
        'designation': designation,
        'department': department,
        'reporting': reporting,
        'address': address,
        'job_grade': job_grade,
        'hr_name': hr_name,
        'offer_accept_date': offer_accept_date,
        'mobile_no': mobile_no,
        'formatted_date':formatted_date,
        'offer_letter_id':offer_letter_id
    })
###########################################Payroll###################################################
@login_required(login_url='do_login')
@require_user_type(1)
def payroll(request):
    template_name = 'hr_management/admin/payroll.html'
    context = {}
    return render(request,template_name, context)

###########################################Generate wage register ###################################################

@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def employee_wage_register_details(request):
    try:
        employees = Employee_Onboarding.objects.all()
        wage_registers = []
        for employee in employees:
            last_wage_register = WageRegister.objects.filter(employee_id=employee.employee_id).order_by('-id').first()
            wage_registers.append(last_wage_register)
            month = last_wage_register.month
            year = last_wage_register.year
        for wage_register in wage_registers:
            wage_register.new_days_payable = int(wage_register.days_payable) - int(wage_register.sunday_and_holidays)
        if request.user.user_type == '1':
            return render(request, 'hr_management/admin/wage_register.html', {'employees': employees, 'wage_registers': wage_registers,'month':month,'year':year})
        else:
            return render(request, 'hr_management/hr/wage_register.html', {'employees': employees, 'wage_registers': wage_registers,'month':month,'year':year})
    except:
        return HttpResponse("Invalid request")
        

@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def wage_register(request):
    try:
        employees = Employee_Onboarding.objects.filter(employee__admin__is_active=True)  
        # employees = Employee_Onboarding.objects.all()
        employees = sorted(employees, key=lambda emp: emp.employee.emp_id)
        wage_registers = []
        today = date.today()
        salary_drop = SalarySlip.objects.all()
        available_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        current_year = datetime.now().year
        available_years = [str(year) for year in range(current_year-1, current_year + 2)]

        remaining_years = {}
        for year in available_years:
            remaining_months = []
            for month in available_months:
                if not any(w.year == year and w.month == month for w in salary_drop):
                    remaining_months.append(month)
            if remaining_months:
                remaining_years[year] = remaining_months

        if request.method == "POST":
            month = request.POST.get('month_name')
            year = int(request.POST.get('year'))
            days_payable = int(request.POST.get('days'))
            days_paid = int(request.POST.get('paid'))

            month_index = available_months.index(month.capitalize()) + 1

            # Calculate the number of Sundays in the selected month
            _, num_days = calendar.monthrange(year, month_index)
            first_weekday = calendar.weekday(year, month_index, 1)
            num_sundays = (num_days - (6 - first_weekday)) // 7
            if (num_days - (6 - first_weekday)) % 7 > 0:
                num_sundays += 1

            month_to_number = {
                'january': 1,
                'february': 2,
                'march': 3,
                'april': 4,
                'may': 5,
                'june': 6,
                'july': 7,
                'august': 8,
                'september': 9,
                'october': 10,
                'november': 11,
                'december': 12
            }

            month_number = month_to_number.get(month.lower())
            existing_data = WageRegister.objects.filter(month=month, year=year)
            existing_data.delete()


            for employee in employees:
                if not employee.employee.admin.is_active:
                    continue 
                employee_id = employee.id
                onboarding_data = Employee_Onboarding.objects.get(id=employee_id)
                contact_no = onboarding_data.contact_no
                emergency_contact_no = onboarding_data.emergency_contact_no
                offer = OfferLetter_Sended.objects.get(mobile_no=contact_no)
                # offer = OfferLetter_Sended.objects.filter(Q(mobile_no=contact_no) | Q(emergency_contact_no=emergency_contact_no))
                ctc = offer.ctc
                address = offer.address

                age = today.year - employee.dob.year

                # Check if the birth month and day have already passed in the current year
                if today.month < employee.dob.month or (today.month == employee.dob.month and today.day < employee.dob.day):
                    age -= 1
                age = age

                if employee_id:
                    onboarding_data = get_object_or_404(Employee_Onboarding, id=employee_id)
                    employee = onboarding_data.employee

                    if ctc <= 273700:
                        insurance_premiums = 0
                    else:
                        insurance_premiums = 11000.0

                    variable_component = (ctc * 0.10)
                    total_variable_pay = ctc * 0.10
                    total_fixed_pay = ctc - total_variable_pay - insurance_premiums
                    basic_pay = total_fixed_pay * 0.40
                    employer_pf_contribution = 0.13 * basic_pay
                    hra = 0.50 * basic_pay
                    if ctc <=  273700:
                        total_flexible_component = total_fixed_pay - basic_pay - hra - employer_pf_contribution - (offer.ctc * 0.0325)
                        # total_flexible_component = total_fixed_pay - basic_pay - hra - employer_pf_contribution - (total_fixed_pay * 0.0325)
                    else:
                        total_flexible_component = total_fixed_pay - basic_pay - hra - employer_pf_contribution
                    conveyance_allowance = 1600 / int(days_payable) * int(days_paid)
                    professional_tax = 200
                    income_tax = 0

                    total_variable_pay = ctc * 0.10
                    total_fixed_pay = ((ctc) - (insurance_premiums + variable_component)) / 12 * int(days_paid) / int(days_payable)
                    basic_salary = (total_fixed_pay * 0.40)
                    variable_component = (ctc * 0.10) / 12 * int(days_paid) / int(days_payable)
                    hra = 0.50 * basic_salary
                    provident_fund = 0.12 * basic_salary
                    flexible_component = (total_flexible_component / 12) * days_paid / days_payable - conveyance_allowance
                    gross_salary = (hra + basic_salary + conveyance_allowance + flexible_component + variable_component)
                    flexible_component = gross_salary - basic_salary - hra - conveyance_allowance - variable_component
                    other_deductions = 0
                    if ctc <= 273700:
                        esic = (0.0075 * float(gross_salary))
                    else:
                        esic = 0
                    total_deductions = provident_fund + professional_tax + income_tax + other_deductions +esic
                    net_salary = Decimal(gross_salary) - Decimal(total_deductions)

                    ytd_net_salary = net_salary
                    ytd_basic_salary = basic_salary
                    ytd_hra = hra
                    ytd_conveyance_allowance = conveyance_allowance
                    ytd_flexible_component = flexible_component
                    ytd_variable_component = variable_component
                    ytd_provident_fund = provident_fund
                    ytd_esic = esic
                    ytd_professional_tax = professional_tax
                    ytd_income_tax = income_tax
                    ytd_other_deductions = other_deductions
                    ytd_total_deductions = total_deductions
                    ytd_gross_salary = gross_salary

                    prev_wage_register = WageRegister.objects.filter(employee_id=employee).order_by('-id')[0:1]

                    if prev_wage_register:
                        first_salary_slip = prev_wage_register[0]
                        net_salary = first_salary_slip.net_salary
                        ytd_net_salary = first_salary_slip.ytd_net_salary
                        basic_salary = first_salary_slip.basic_salary
                        ytd_basic_salary = first_salary_slip.ytd_basic_salary
                        hra = first_salary_slip.hra
                        ytd_hra = first_salary_slip.ytd_hra
                        conveyance_allowance = first_salary_slip.conveyance_allowance
                        ytd_conveyance_allowance = first_salary_slip.ytd_conveyance_allowance
                        flexible_component = first_salary_slip.flexible_component
                        ytd_flexible_component = first_salary_slip.ytd_flexible_component
                        variable_component = first_salary_slip.variable_component
                        ytd_variable_component = first_salary_slip.ytd_variable_component
                        provident_fund = first_salary_slip.provident_fund
                        ytd_provident_fund = first_salary_slip.ytd_provident_fund
                        esic = first_salary_slip.esic
                        ytd_esic = first_salary_slip.ytd_esic
                        professional_tax = first_salary_slip.professional_tax
                        ytd_professional_tax = first_salary_slip.ytd_professional_tax
                        income_tax = first_salary_slip.income_tax
                        ytd_income_tax = first_salary_slip.ytd_income_tax
                        other_deductions = first_salary_slip.other_deductions
                        ytd_other_deductions = first_salary_slip.ytd_other_deductions
                        total_deductions = first_salary_slip.total_deductions
                        ytd_total_deductions = first_salary_slip.ytd_total_deductions
                        gross_salary = first_salary_slip.gross_salary
                        ytd_gross_salary = first_salary_slip.ytd_gross_salary

                        if month_number == 4:  # Check if the month is April or later
                            ytd_net_salary = net_salary
                            ytd_basic_salary = basic_salary
                            ytd_hra = hra
                            ytd_conveyance_allowance = conveyance_allowance
                            ytd_flexible_component = flexible_component
                            ytd_variable_component = variable_component
                            ytd_provident_fund = provident_fund
                            ytd_esic = esic
                            ytd_professional_tax = professional_tax
                            ytd_income_tax = income_tax
                            ytd_other_deductions = other_deductions
                            ytd_total_deductions = total_deductions
                            ytd_gross_salary = gross_salary
                        else:
                            ytd_net_salary += net_salary
                            ytd_basic_salary += basic_salary
                            ytd_hra += hra
                            ytd_conveyance_allowance += conveyance_allowance
                            ytd_flexible_component += flexible_component
                            ytd_variable_component += variable_component
                            ytd_provident_fund += provident_fund
                            ytd_esic += esic
                            ytd_professional_tax += professional_tax
                            ytd_income_tax += income_tax
                            ytd_other_deductions += other_deductions
                            ytd_total_deductions += total_deductions
                            ytd_gross_salary += gross_salary

                    wage_register = WageRegister(
                        employee_id=employee,
                        month=month,
                        sunday_and_holidays = num_sundays,
                        year=year,
                        age = age,
                        days_payable=days_payable,
                        days_paid=days_paid,
                        ctc=round(ctc),
                        esic=round(esic),
                        basic_salary=round(basic_salary),
                        hra=round(hra),
                        conveyance_allowance=round(conveyance_allowance),
                        flexible_component=round(flexible_component),
                        variable_component=round(variable_component),
                        provident_fund=round(provident_fund),
                        professional_tax=round(professional_tax),
                        income_tax=round(income_tax),
                        other_deductions=round(other_deductions),
                        gross_salary=round(gross_salary),
                        total_deductions=round(total_deductions),
                        net_salary=round(net_salary),
                        address=address,
                        ytd_net_salary=round(ytd_net_salary),
                        ytd_basic_salary=round(ytd_basic_salary),
                        ytd_hra=round(ytd_hra),
                        ytd_conveyance_allowance=round(ytd_conveyance_allowance),
                        ytd_flexible_component=round(ytd_flexible_component),
                        ytd_variable_component=round(ytd_variable_component),
                        ytd_provident_fund=round(ytd_provident_fund),
                        ytd_esic=round(ytd_esic),
                        ytd_professional_tax=round(ytd_professional_tax),
                        ytd_income_tax=round(ytd_income_tax),
                        ytd_other_deductions=round(ytd_other_deductions),
                        ytd_total_deductions=round(ytd_total_deductions),
                        ytd_gross_salary=round(ytd_gross_salary)
                    )
                    wage_register.save()
                    wage_registers.append(wage_register)
                    wage_register.new_days_payable = wage_register.days_payable - wage_register.sunday_and_holidays
            
            if request.user.user_type == '1':
                return render(request, 'hr_management/admin/wage_register.html', {'employees': employees, 'wage_registers': wage_registers,'age':age,'month':month,'year':year,'days_payable':days_payable})
            else:
                return render(request, 'hr_management/hr/wage_register.html', {'employees': employees, 'wage_registers': wage_registers,'age':age,'month':month,'year':year,'days_payable':days_payable})
        if request.user.user_type == '1':
            return render(request, 'hr_management/admin/employee_salary_all.html', {'employees': employees,'remaining_years':remaining_years})
        else:
            return render(request, 'hr_management/hr/employee_salary_all.html', {'employees': employees,'remaining_years':remaining_years})
    except BaseException as a:
        print(a,'aaaaaaaaaa')
        messages.error(request,"May be something went to wrong")
        return HttpResponseRedirect(reverse("wage_register"))



@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def old_wage_register(request):
    salary_slips = WageRegister.objects.all()
    unique_months = set()
    unique_years = set()
    for slip in salary_slips:
            unique_months.add(slip.month)
            unique_years.add(slip.year)

    if request.method == 'POST':    
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        if selected_month:
            salary_slips = salary_slips.filter(month=selected_month)

        if selected_year:
            salary_slips = salary_slips.filter(year=selected_year)

        old_wage_registers = salary_slips
        selected_salary_slip = old_wage_registers.first()
        if not selected_salary_slip:
            if request.user.user_type == '2':
                return render(request, 'hr_management/hr/wage_register_not_generated.html')
            else:
                return render(request, 'hr_management/admin/wage_register_not_generated.html')
            
        if request.user.user_type == '1':
            return render(request, 'hr_management/admin/old_wage_register.html', {
                "salary_slips": salary_slips,
                "old_wage_registers": old_wage_registers,
                "selected_salary_slip": selected_salary_slip,
                "unique_months": unique_months,  # Pass unique_months to the template
                "unique_years": unique_years,  # Pass unique_years to the template
            })
        else:
            return render(request, 'hr_management/hr/old_wage_register.html', {
                "salary_slips": salary_slips,
                "old_wage_registers": old_wage_registers,
                "selected_salary_slip": selected_salary_slip,
                "unique_months": unique_months,  # Pass unique_months to the template
                "unique_years": unique_years,  # Pass unique_years to the template
            })
    output_month_sorted = sorted(unique_months, key=lambda x: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'].index(x))
    output_year_sorted = sorted(list(unique_years))
    if request.user.user_type == '1':
        return render(request, 'hr_management/admin/old_wage_register.html',{'unique_months':output_month_sorted,"unique_years": output_year_sorted})
    else:
        return render(request, 'hr_management/hr/old_wage_register.html',{'unique_months':output_month_sorted,"unique_years": output_year_sorted})

#########################################################################################################################
@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def generate_salary_slips(request):
    try:
        active_employees = Employees.objects.filter(employee_onboarding__employee__admin__is_active=True)
        salary_slips = []
        for employee in active_employees:
            wage_register = WageRegister.objects.filter(employee_id=employee).last()

            if wage_register is not None:
                employee_id = wage_register.employee_id.id
                onboarding_data = Employee_Onboarding.objects.get(employee_id=employee_id)
                # onboarding_data = Employee_Onboarding.objects.get(employee_id=employee.id)
                c = onboarding_data.contact_no
                offer = OfferLetter_Sended.objects.get(mobile_no=c)
                address = offer.address

                salary_slip = SalarySlip(
                    employee_id=employee,
                    basic_salary=wage_register.basic_salary,
                    conveyance_allowance=wage_register.conveyance_allowance,
                    total_deductions=wage_register.total_deductions,
                    gross_salary=wage_register.gross_salary,
                    net_salary=wage_register.net_salary,
                    ctc=wage_register.ctc,
                    hra=wage_register.hra,
                    esic=wage_register.esic,
                    flexible_component=wage_register.flexible_component,
                    variable_component=wage_register.variable_component,
                    provident_fund=wage_register.provident_fund,
                    professional_tax=wage_register.professional_tax,
                    income_tax=wage_register.income_tax,
                    other_deductions=wage_register.other_deductions,
                    other_allowns=wage_register.other_allowns,
                    lwf=wage_register.lwf,
                    ytd_ctc=wage_register.ytd_ctc,
                    ytd_hra=wage_register.ytd_hra,
                    ytd_esic=wage_register.ytd_esic,
                    ytd_basic_salary=wage_register.ytd_basic_salary,
                    ytd_conveyance_allowance=wage_register.ytd_conveyance_allowance,
                    ytd_flexible_component=wage_register.ytd_flexible_component,
                    ytd_variable_component=wage_register.ytd_variable_component,
                    ytd_provident_fund=wage_register.ytd_provident_fund,
                    ytd_professional_tax=wage_register.ytd_professional_tax,
                    ytd_income_tax=wage_register.ytd_income_tax,
                    ytd_other_deductions=wage_register.ytd_other_deductions,
                    ytd_gross_salary=wage_register.ytd_gross_salary,
                    ytd_total_deductions=wage_register.ytd_total_deductions,
                    ytd_net_salary=wage_register.ytd_net_salary,
                    days_payable=wage_register.days_payable,
                    days_paid=wage_register.days_paid,
                    address=address,
                    month=wage_register.month,
                    year=wage_register.year,
                )
                salary_slip.save()
                salary_slips.append(salary_slip)
        if request.user.user_type == '2':
            return render(request, 'hr_management/hr/salary_slip_generate_successfully.html')
        else:
            return render(request, 'hr_management/admin/salary_slip_generate_successfully.html')
    except:
        messages.success(request,"May be something went to wrong")
        return HttpResponseRedirect(reverse("generate_salary_slips"))
    
# ################################Update wage register ##############################################
@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])               
def edit_wage_register(request, pk):
    try:
        wage_register = get_object_or_404(WageRegister, id=pk)
        employees = Employee_Onboarding.objects.all()

        if request.method == "POST":
            ctc = float(request.POST.get('ctc'))
            wage_register.month = request.POST.get('month')
            wage_register.year = request.POST.get('year')
            days_payable = Decimal(request.POST.get('days_payable'))
            days_paid = Decimal(request.POST.get('days_paid'))
            wage_register.days_payable = days_payable
            wage_register.days_paid = days_paid
            wage_register.basic_salary = Decimal(request.POST.get('basic_salary'))
            wage_register.hra = Decimal(request.POST.get('hra'))
            wage_register.conveyance_allowance = Decimal(request.POST.get('conveyance_allowance'))
            wage_register.variable_component = Decimal(request.POST.get('variable_component'))
            wage_register.other_allowns = Decimal(request.POST.get('other_allowns'))
            wage_register.gross_salary = Decimal(request.POST.get('gross_salary'))
            wage_register.provident_fund = Decimal(request.POST.get('provident_fund'))
            wage_register.professional_tax = Decimal(request.POST.get('professional_tax'))
            wage_register.income_tax = Decimal(request.POST.get('income_tax'))
            wage_register.lwf = Decimal(request.POST.get('lwf'))
            wage_register.other_deductions = Decimal(request.POST.get('other_deductions'))
            wage_register.net_salary = Decimal(request.POST.get('net_salary'))
            wage_register.esic = Decimal(request.POST.get('esic'))
            wage_register.sunday_and_holidays = int(request.POST.get('sunday_and_holidays'))

            check_box = request.POST.get('check_box')   
            hra = 0
            esic = 0
            basic_salary = 0
            conveyance_allowance = 0
            flexible_component = 0
            variable_component = 0
            provident_fund = 0
            professional_tax = 0
            income_tax = 0
            other_deductions = 0
            gross_salary = 0
            total_deductions = 0
            net_salary = 0

            ytd_hra = hra
            ytd_ctc = ctc
            ytd_esic = esic
            ytd_basic_salary = basic_salary
            ytd_conveyance_allowance = conveyance_allowance
            ytd_flexible_component = flexible_component
            ytd_variable_component = variable_component
            ytd_provident_fund = provident_fund
            ytd_professional_tax = professional_tax
            ytd_income_tax = income_tax
            ytd_other_deductions = other_deductions
            ytd_gross_salary = gross_salary

            ytd_total_deductions = total_deductions
            ytd_net_salary = net_salary

            for employee in employees:
                employee_id = employee.id

                if employee_id:
                        if ctc <= 273700:
                            insurance_premiums = 0
                        else:
                            insurance_premiums = 11000.0
                        total_variable_pay = ctc * 0.10
                        total_fixed_pay = ctc - total_variable_pay - insurance_premiums
                        basic_pay = total_fixed_pay * 0.40
                        employer_pf_contribution = 0.13 * basic_pay
                        hra = 0.50 * basic_pay
                        total_flexible_component = total_fixed_pay - basic_pay - hra - employer_pf_contribution  
                        conveyance_allowance = 1600/ int(days_payable) * int(days_paid)
                        professional_tax = 200
                        income_tax = float(wage_register.income_tax)

                        total_fixed_pay = ((ctc) - (insurance_premiums + total_variable_pay)) / 12 * int(days_paid)/int(days_payable)
                        basic_salary = (total_fixed_pay * 0.40)
                        if check_box =='true':
                            variable_component = wage_register.variable_component
                        else:
                            variable_component = (ctc * 0.10) / 12 * int(days_paid) / int(days_payable)

                        hra = 0.50 * basic_salary
                        wage_register.ytd_hra = hra + float(wage_register.ytd_hra)
                        wage_register.ytd_ctc = ctc + float(wage_register.ytd_ctc)
                        wage_register.ytd_esic = esic + float(wage_register.ytd_esic)
                        wage_register.ytd_basic_salary = basic_salary+ float(wage_register.ytd_basic_salary)
                        wage_register.ytd_conveyance_allowance = conveyance_allowance
                        wage_register.ytd_flexible_component = flexible_component
                        wage_register.ytd_variable_component = variable_component
                        wage_register.ytd_provident_fund = provident_fund
                        wage_register.ytd_professional_tax = professional_tax
                        wage_register.ytd_income_tax = income_tax
                        wage_register.ytd_other_deductions = float(other_deductions)
                        wage_register.ytd_gross_salary = gross_salary
                        wage_register.ytd_total_deductions = total_deductions
                        wage_register.ytd_net_salary = net_salary
                    
                        provident_fund = 0.12 * basic_salary
                        flexible_component= float((total_flexible_component / 12) * int(days_paid)/int(days_payable) - conveyance_allowance)
                        gross_salary = round(hra + basic_salary + conveyance_allowance + flexible_component + variable_component)
                        if ctc <=  273700:
                            flexible_component = float(gross_salary) - float(basic_salary) - float(hra) - float(conveyance_allowance) - float(variable_component) - float((ctc/12 * 0.0325)*int(days_paid)/int(days_payable))
                            # flexible_component = float(gross_salary) - float(basic_salary) - float(hra) - float(conveyance_allowance) - float(variable_component) - float(( total_fixed_pay/12 * 0.0325)*int(days_paid)/int(days_payable))

                        else:
                            flexible_component = float(gross_salary) - float(basic_salary) - float(hra) - float(conveyance_allowance) - float(variable_component)
                        
                        gross_salary = float(hra) + float(basic_salary) + float(conveyance_allowance) + float(flexible_component) + float(variable_component)
            
                        if ctc <= 273700:
                            esic = 0.0075 * float(gross_salary)

                        else:
                            esic = 0
                        other_deductions = wage_register.other_deductions
                        total_deductions = provident_fund + professional_tax + income_tax + float(other_deductions)+ esic
                        wage_register.basic_salary=round(basic_salary)
                        wage_register.hra= round(hra)
                        wage_register.conveyance_allowance= round(conveyance_allowance)
                        wage_register.variable_component= round(variable_component)
                        wage_register.gross_salary= round(gross_salary)
                        wage_register.flexible_component= round(flexible_component) 
                        wage_register.professional_tax = round( professional_tax)
                        wage_register.provident_fund = round( provident_fund)
                        wage_register.total_deductions = round(total_deductions)
                        wage_register.esic = round(esic)
                        net_salary = round(float(wage_register.gross_salary) -float(wage_register.total_deductions))
                        wage_register.net_salary = round(net_salary)
                                                

                        wage_register.ytd_hra = round(ytd_hra)
                        wage_register.ytd_ctc = round(ytd_ctc) 
                        wage_register.ytd_esic = round(ytd_esic)
                        wage_register.ytd_basic_salary= round(ytd_basic_salary)
                        wage_register.ytd_conveyance_allowance = round(ytd_conveyance_allowance)
                        wage_register.ytd_variable_component = round(ytd_variable_component)
                        wage_register.ytd_provident_fund = round(ytd_provident_fund)
                        wage_register.ytd_professional_tax = round(ytd_professional_tax)
                        wage_register.ytd_income_tax = round(ytd_income_tax)
                        wage_register.ytd_other_deductions = round(ytd_other_deductions)
                        wage_register.ytd_total_deductions = round(ytd_total_deductions)
                        wage_register.ytd_gross_salary = round(ytd_gross_salary)
                        wage_register.ytd_net_salary = round(ytd_net_salary)
                        wage_register.ytd_flexible_component = round(ytd_flexible_component)

                        if wage_register.month == 'April':  # Check if the month is April or later
                            wage_register.ytd_basic_salary = round(basic_salary)
                            wage_register.ytd_hra = round(hra)
                            wage_register.ytd_ctc = round(ctc)
                            wage_register.ytd_net_salary = round(net_salary)
                            wage_register.ytd_conveyance_allowance = round(conveyance_allowance)
                            wage_register.ytd_flexible_component = round(flexible_component)
                            wage_register.ytd_variable_component = round(variable_component)
                            wage_register.ytd_provident_fund = round(provident_fund)
                            wage_register.ytd_esic = round(esic)
                            wage_register.ytd_professional_tax = round(professional_tax)
                            wage_register.ytd_income_tax = round(income_tax)
                            wage_register.ytd_other_deductions = round(other_deductions)
                            wage_register.ytd_total_deductions = round(total_deductions)
                            wage_register.ytd_gross_salary = round(gross_salary)
                            wage_register.ytd_net_salary = round(net_salary)

                            
                        else:
                            wage_register.ytd_net_salary += round(int(net_salary))
                            wage_register.ytd_basic_salary += round(int(basic_salary))
                            wage_register.ytd_hra += round(Decimal(hra))
                            wage_register.ytd_ctc += round(Decimal(ctc))
                            wage_register.ytd_conveyance_allowance += round(Decimal(conveyance_allowance))
                            wage_register.ytd_flexible_component += round(Decimal(flexible_component))
                            wage_register.ytd_variable_component += round(Decimal(variable_component))
                            wage_register.ytd_provident_fund += round(Decimal(provident_fund))
                            wage_register.ytd_esic += round(float(esic))
                            wage_register.ytd_professional_tax += round(Decimal(professional_tax))
                            wage_register.ytd_income_tax += round(Decimal(income_tax))
                            wage_register.ytd_other_deductions += round(Decimal(other_deductions))
                            wage_register.ytd_total_deductions += round(Decimal(total_deductions))
                            wage_register.ytd_gross_salary += round(Decimal(gross_salary))

                        wage_register.save() 
                        previous_wage_registers = {}
                        wage_registers = WageRegister.objects.filter(employee_id=wage_register.employee_id).order_by('-id')

                        for idx, wage_register in enumerate(wage_registers):
                            if idx != 0:
                                previous_wage_registers[int(wage_register.id)] = int(wage_registers[idx - 1].id)
                        pre_salary = list(previous_wage_registers.keys())

                        wage_register1 = WageRegister.objects.get(id=pk)
                        wage_register2 = None  # Initialize wage_register2 with a default value

                        try:
                            wage_register2 = WageRegister.objects.get(id=pre_salary[0])
                        except:
                            pass
                        if wage_register2:
                            wage_register1.ytd_hra += round(wage_register2.ytd_hra)
                            wage_register1.ytd_esic += round(wage_register2.ytd_esic)
                            wage_register1.ytd_ctc += round(wage_register2.ytd_ctc)
                            wage_register1.ytd_basic_salary += round(wage_register2.ytd_basic_salary)
                            wage_register1.ytd_conveyance_allowance += round(wage_register2.ytd_conveyance_allowance)
                            wage_register1.ytd_variable_component += round(wage_register2.ytd_variable_component)
                            wage_register1.ytd_provident_fund += round(wage_register2.ytd_provident_fund)
                            wage_register1.ytd_professional_tax += round(wage_register2.ytd_professional_tax)
                            wage_register1.ytd_income_tax += round(wage_register2.ytd_income_tax)
                            wage_register1.ytd_other_deductions += round(wage_register2.ytd_other_deductions)
                            wage_register1.ytd_total_deductions += round(wage_register2.ytd_total_deductions)
                            wage_register1.ytd_gross_salary += round(wage_register2.ytd_gross_salary)
                            wage_register1.ytd_net_salary += round(wage_register2.ytd_net_salary)
                            wage_register1.ytd_flexible_component += round(wage_register2.ytd_flexible_component)


                        wage_register1.save()
                        if request.user.user_type == '1':
                            return redirect('employee_wage_register_details')                    
                        else:
                            return redirect('employee_wage_register_details')

        if request.user.user_type == '1':
            return render(request, 'hr_management/admin/edit_wage_register.html', {'wage_register': wage_register})
        else:
            return render(request, 'hr_management/hr/edit_wage_register.html', {'wage_register': wage_register})
    except BaseException as a:
        print(a)



@login_required(login_url='do_login')
@require_user_type(user_type=[3, 4])
def submit_reimbursement_view(request):
    try:
        employee = Employees.objects.get(admin=request.user)
        context = {}
        last_bill = Reimbursement_bill.objects.order_by('-bill_no').first()
        if last_bill:
            next_bill_no = last_bill.bill_no + 1
        else:
            next_bill_no = 1
        context['next_bill_no'] = next_bill_no  
        manager_name = employee.admin.manager
        first_name = employee.admin.first_name
        last_name = employee.admin.last_name
        employee_name = f"{first_name} {last_name}"
        manager_email = CustomUser.objects.filter(username=manager_name).values_list('email', flat=True).first()

        if request.method == 'POST':
            total_amount = request.POST.get('total_amount')
            reimbursement_bill = Reimbursement_bill.objects.create(employee_id=employee, bill_no=next_bill_no, total_amount=total_amount)
            reimbursement_bill.query = f'Pending with {manager_name}'
            reimbursement_bill.save()
            field_count = len([key for key in request.POST.keys() if key.startswith('date')])

            for i in range(1, field_count + 1):
                date = request.POST.get(f'date{i}')
                amount = request.POST.get(f'amount{i}')
                reason = request.POST.get(f'reason{i}')
                attachment = request.FILES.get(f'attachment{i}')
                sr_no = request.POST.get(f'sr_no{i}')
                description = request.POST.get(f'description{i}')

                reimbursement_data = Reimbursement_data.objects.create(
                    employee_id=employee,
                    bill_no=reimbursement_bill,
                    date=date,
                    amount=amount,
                    reason=reason,
                    attachment=attachment,
                    sr_no=sr_no,
                    description=description,  
                )
                reimbursement_data.save()

            # Send email to manager
            email_subject = 'Reimbursement Submission'
            email_template = 'hr_management/admin/send_reimbursement_email.html'  # Replace with the actual path
            email_context = {
                'employee_name': employee_name,
                'bill_no': next_bill_no,
                'manager_name':manager_name,
                'date':date,
                'amount':total_amount,
                'reason':reason,
                'description':description
            }
            email_html_message = render_to_string(email_template, email_context)
            email_plain_message = strip_tags(email_html_message)
            from_email = f'{settings.EMAIL_FROM_NAME} <{getattr(settings, "EMAIL_HOST_USER", "default_from_email")}>'
            to_email = manager_email  # Assuming manager has an email field in the User model
            send_mail(email_subject, email_plain_message, from_email, [to_email], html_message=email_html_message)

            return redirect('reimburesement_history')
        
        if request.user.user_type == '3':
            return render(request, 'hr_management/employee_template/reimbursment_new.html', context)
        else:
            return render(request, 'hr_management/manager_template/reimbursment_new.html', context)
    except Employees.DoesNotExist:
        messages.error(request, "Employee not found.")
    except Exception as e:
        messages.error(request, f"Something went wrong: {e}")

    return redirect('reimburesement_history')


@login_required(login_url='do_login')
@require_user_type(user_type=[3, 4])
def reimburesement_history(request):
    
    employee = Employees.objects.filter(admin=request.user.id).first()
    reimbursement = Reimbursement_bill.objects.filter(employee_id=employee).order_by('-id')
    
    page = request.GET.get('page')
    paginator = Paginator(reimbursement, 10) 
    
    try:
        reimbursement = paginator.page(page)
    except PageNotAnInteger:
        reimbursement = paginator.page(1)
    except EmptyPage:
        reimbursement = paginator.page(paginator.num_pages)
    
    if request.user.user_type == '3':
        return render(request, 'hr_management/employee_template/reimbursemenet_history.html', {'reimbursement': reimbursement})
    else:
        return render(request, 'hr_management/manager_template/reimbursemenet_history.html', {'reimbursement': reimbursement})
    


@login_required(login_url='do_login')
@require_user_type(user_type=[1, 3, 4, 5])
def view_reimbursement(request, id):
    try:
        record = Reimbursement_data.objects.filter(bill_no_id=id)
        records = Reimbursement_bill.objects.filter(id=id )
        if request.user.user_type == '4':
            return render(request, 'hr_management/manager_template/reimbursment_details_emp.html', {'record': record,'records':records})
        if request.user.user_type == '5':
            return render(request, 'hr_management/account_template/reimbursment_details_emp.html', {'record': record,'records':records})
        if request.user.user_type == '1':
            return render(request, 'hr_management/admin/reimbursment_details_emp.html', {'record': record,'records':records})
        else:
            return render(request, 'hr_management/employee_template/reimbursment_details.html', {'record': record,'records':records})
    except BaseException as a:
        print(a)
    return HttpResponseNotFound("Page not found")

@login_required(login_url='do_login')
@require_user_type(user_type=[1, 3, 4, 5])
def view_reimbursement_manager(request, id):
    reimbursment_data = Reimbursement_data.objects.filter(bill_no_id=id)
    reimbursment_bill = Reimbursement_bill.objects.filter(id=id )
    
    return render(request, 'hr_management/manager_template/reimbursment_details.html', {'record': reimbursment_data,'records':reimbursment_bill})


@login_required(login_url='do_login')
@require_user_type(user_type=[1, 4])
def employee_approve_reimbursement(request, id):
    try:
        records = Reimbursement_bill.objects.filter(id=id)
        account_user = CustomUser.objects.filter(user_type=5).first()
        for record in records:
            first_name = record.employee_id.admin.first_name 
            last_name = record.employee_id.admin.last_name
            employee_name = f"{first_name} {last_name}"
            account_email = account_user.email
            employee_email = record.employee_id.admin.email
            bill_no = record.bill_no
            record.reimbursement_status = 1
            record.approved_by = f"{request.user.first_name} {request.user.last_name}"
            record.query = f'Approved by {request.user.first_name} {request.user.last_name}, Pending with Accounts.'
            send_reimbursement_approval_email(employee_email,bill_no,account_email,employee_name)
            record.save()
        return redirect('manage_reimbursement_view')
    except BaseException as a:
        print(a)

def send_reimbursement_approval_email(employee_email,bill_no,account_email,employee_name):
    try:
        # Construct the email content
        email_subject = 'Reimbursement Approval From Manager'
        application_link = 'http://app1.olatechs.com:8080/'
        email_template = 'hr_management/manager_template/send_employee_reimbursement_email.html'
        email_context = {
            "bill_no" : bill_no,
            "employee_name":employee_name,    
            'application_link':application_link,
        }
        email_html_message = render_to_string(email_template, email_context)
        email_plain_message = strip_tags(email_html_message)
        from_email = f'{settings.EMAIL_FROM_NAME} <{getattr(settings, "EMAIL_HOST_USER", "default_from_email")}>'
        to_email = employee_email # Replace with the recipient's email address
        send_mail(email_subject, email_plain_message, from_email, [to_email], html_message=email_html_message)

        email_subject_account = 'Reimbursement Approval From Manager'
        email_template_account = 'hr_management/manager_template/send_account_reimbursement_email.html'
        email_context_account = {
            "bill_no": bill_no,
            "employee_name":employee_name,
        }
        email_html_message_account = render_to_string(email_template_account, email_context_account)
        email_plain_message_account = strip_tags(email_html_message_account)
        send_mail(email_subject_account,email_plain_message_account,from_email,[account_email],html_message=email_html_message_account)
    except BaseException as a:
        print(a)


@login_required(login_url='do_login')
@require_user_type(user_type=[1, 4])
def employee_disapprove_reimbursement(request, id):     
    record = get_object_or_404(Reimbursement_bill, id=id)
    bill_no = record.bill_no
    employee_email = record.employee_id.admin.email
    if request.method == 'POST':
        first_name = record.employee_id.admin.first_name 
        last_name = record.employee_id.admin.last_name
        employee_name = f"{first_name} {last_name}"
        query = request.POST.get('query')
        record.query = f'Rejected by {request.user.first_name} {request.user.last_name} reason is {query}' 
        record.reimbursement_status = 2
        send_reimbursement_disapproval_email(employee_email,bill_no,employee_name)
        record.save()
        return redirect('manage_reimbursement_view')
    return HttpResponseRedirect(reverse("manage_reimbursement_view"))


def send_reimbursement_disapproval_email(employee_email,bill_no,employee_name):
    # Construct the email content
    email_subject = 'Reimbursement Sent Back From Manager'
    application_link = 'http://app1.olatechs.com:8080/'
    email_template = 'hr_management/manager_template/send_employee_reimbursement_email_rejected.html'  # Replace with the actual path
    email_context = {
        "bill_no" : bill_no,
        'employee_name':employee_name,
        'application_link':application_link,
    }
    email_html_message = render_to_string(email_template, email_context)
    email_plain_message = strip_tags(email_html_message)
    from_email = f'{settings.EMAIL_FROM_NAME} <{getattr(settings, "EMAIL_HOST_USER", "default_from_email")}>'
    to_email = employee_email  # Replace with the recipient's email address
    send_mail(email_subject, email_plain_message, from_email, [to_email], html_message=email_html_message)


@login_required(login_url='do_login')
@require_user_type(user_type=[3, 4])
def edit_reimbursement(request, id):
    record = get_object_or_404(Reimbursement_bill, id=id)
    employee = Employees.objects.get(admin=request.user)
    records = Reimbursement_data.objects.filter(bill_no=record)
    records1 = Reimbursement_bill.objects.filter(id=id)
    manager_name = employee.admin.manager
    first_name = employee.admin.first_name
    last_name = employee.admin.last_name
    employee_name = f"{first_name} {last_name}"
    manager_email = CustomUser.objects.filter(username=manager_name).values_list('email', flat=True).first()
    if request.method == 'POST':
        new_bill_no = request.POST.get('bill_no')
        record.bill_no = new_bill_no
        record.save()

        total_amount = float(request.POST.get('total_amount'))
        record.total_amount = total_amount
        record.save()
    
        for entry in records:
            date = request.POST.get(f'date{entry.id}')
            amount = request.POST.get(f'amount{entry.id}')
            reason = request.POST.get(f'reason{entry.id}')
            attachment = request.FILES.get(f'attachment{entry.id}')
            sr_no = request.POST.get(f'sr_no{entry.id}')
            description = request.POST.get(f'description{entry.id}')

            entry.date = date
            entry.amount = amount
            entry.reason = reason
            entry.sr_no = sr_no
            entry.description=description
            if attachment:
                entry.attachment = attachment
            
            entry.save()
            
            if f'delete{entry.id}' in request.POST:
                entry.delete()
                
        existing_record_count = records.count()

        field_count = len([key for key in request.POST.keys() if key.startswith('date')])

        for i in range(existing_record_count, field_count + 1):
            date = request.POST.get(f'date{i}')
            amount = request.POST.get(f'amount{i}')
            reason = request.POST.get(f'reason{i}')
            attachment = request.FILES.get(f'attachment{i}')
            sr_no = request.POST.get(f'sr_no{i}')
            description = request.POST.get(f'description{i}')

            reimbursement_data = Reimbursement_data.objects.create(
                employee_id=employee,
                bill_no=record,
                date=date,
                amount=amount,
                reason=reason,
                attachment=attachment,
                sr_no=sr_no,
                description=description,     
            )
            reimbursement_data.save()
        for record in records1:
            record.reimbursement_status = 0 
            email_subject = 'Reimbursement Submission'
            email_template = 'hr_management/admin/send_reimbursement_email.html'  # Replace with the actual path
            email_context = {
                'employee_name': employee_name,
                'bill_no': record.bill_no,
                'manager_name':manager_name,
                'date':date,
                'amount':amount,
                'reason':reason,
                'description':description
            }
            email_html_message = render_to_string(email_template, email_context)
            email_plain_message = strip_tags(email_html_message)
            from_email = f'{settings.EMAIL_FROM_NAME} <{getattr(settings, "EMAIL_HOST_USER", "default_from_email")}>'
            to_email = manager_email  # Assuming manager has an email field in the User model
            send_mail(email_subject, email_plain_message, from_email, [to_email], html_message=email_html_message)
            record.save()
        return redirect('reimburesement_history')
    if request.user.user_type == '3':
        return render(request, 'hr_management/employee_template/reimbursment_details_edit.html', {'record': record, 'records': records})
    else:
        return render(request, 'hr_management/manager_template/reimbursment_details_edit.html', {'record': record, 'records': records})


@login_required(login_url='do_login')
@require_user_type(user_type=[3, 4])
def delete_reimbursement(request, id):
    try:
        reimbursement_record = get_object_or_404(Reimbursement_bill, id=id)
        if request.user == reimbursement_record.employee_id.admin or request.user == reimbursement_record.employee_id.admin.manager:
            reimbursement_data_records = Reimbursement_data.objects.filter(bill_no=reimbursement_record)
            for data_record in reimbursement_data_records:
                if data_record.attachment:
                    data_record.attachment.delete()
                data_record.delete()
            reimbursement_record.delete()
            messages.success(request, "Reimbursement claim deleted successfully.")
        else:
            messages.error(request, "You do not have permission to delete this reimbursement claim.")
    except Reimbursement_bill.DoesNotExist:
        messages.error(request, "Reimbursement claim not found.")
    except Exception as e:
        messages.error(request, f"Something went wrong: {e}")
    return redirect('reimburesement_history')



@login_required(login_url='do_login')
@require_user_type(user_type=4)
def employees_under_manager(request):
    try:
        manager_name = request.user.username
        employees = CustomUser.objects.filter(manager=manager_name,is_active=True)
        return render(request,'hr_management/manager_template/employees_under_manager.html',{ 'employees':employees })
    except BaseException as a:
        print(a)


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2,4])
def employee_leave_count(request, employee_id=None):
    try:
        selected_employee = CustomUser.objects.get(id=employee_id)
        emp = Employees.objects.get(admin_id=employee_id)
        employee_leave_data = EmployeeLeave.objects.filter(employee_id=emp.id)
        leave_report_data = LeaveReportEmployee.objects.filter(employee_id=emp.id).order_by('-id')
        if request.user.user_type == '2':
            return render(request, 'hr_management/hr/employee_leave_count.html', {
                'selected_employee': selected_employee,
                'employee_leave_data': employee_leave_data,
                'leave_report_data':leave_report_data,
            })
        elif request.user.user_type == '4':
            return render(request, 'hr_management/manager_template/employee_leave_count.html', {
                'selected_employee': selected_employee,
                'employee_leave_data': employee_leave_data,
                'leave_report_data':leave_report_data,
            })
        else:
            return render(request, 'hr_management/admin/employee_leave_count.html', {
                'selected_employee': selected_employee,
                'employee_leave_data': employee_leave_data,
                'leave_report_data':leave_report_data,
            })

    except BaseException as a:
        print(a)


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def all_employee_salary_slip(request):
    if request.method == 'POST':
        employee_username = request.POST.get('employee_username')
        year = request.POST.get('year')
        month = request.POST.get('month')

        if employee_username and year and month:
            try:
                employee = Employees.objects.get(admin__username=employee_username)
                salary_slip = SalarySlip.objects.get(
                    employee_id=employee,
                    year=year,
                    month=month
                )
                first_name = employee.admin.first_name
                last_name = employee.admin.last_name
                emp_id = employee.emp_id
                date_of_joining = employee.employee_onboarding.date_of_joining
                emp_department = employee.department
                pancard_no = employee.employee_onboarding.pancard_no
                pf_uan_no = employee.employee_onboarding.pf_uan_no
                emp_designation = employee.designation
                dob = employee.employee_onboarding.dob
                account_number = employee.bankdetails.account_number
                bank_name = employee.bankdetails.bank_name
                net_salary = num2words(salary_slip.net_salary)
                capitalized_word = net_salary.title()
                month_short = month[0:3]
                year_short = year[2:4]
                if request.user.user_type == '1':
                    return render(request, 'hr_management/admin/salary_slip_template.html', {'salary_slip': salary_slip,'first_name':first_name,'last_name':last_name,'emp_id':emp_id,'date_of_joining':date_of_joining,
                                            'emp_department':emp_department,'pancard_no':pancard_no,'pf_uan_no':pf_uan_no,'emp_designation':emp_designation,'dob':dob,'account_number':account_number,
                                            'capitalized_word':capitalized_word,'month_short':month_short,"year_short":year_short,"bank_name":bank_name})
                elif request.user.user_type == '2':
                    return render(request, 'hr_management/hr/salary_slip_template.html', {'salary_slip': salary_slip,'first_name':first_name,'last_name':last_name,'emp_id':emp_id,'date_of_joining':date_of_joining,
                                            'emp_department':emp_department,'pancard_no':pancard_no,'pf_uan_no':pf_uan_no,'emp_designation':emp_designation,'dob':dob,'account_number':account_number,
                                            'capitalized_word':capitalized_word,'month_short':month_short,"year_short":year_short,'bank_name':bank_name})
            except Employees.DoesNotExist:
                error_message = "Employee not found."
            except SalarySlip.DoesNotExist:
                error_message = "Salary slip not found for the selected criteria."
        else:
            error_message = "Please select an employee and provide both year and month."
        # Fetch all usernames to populate the dropdown
        usernames = CustomUser.objects.values_list('username', flat=True).order_by('username')
        return render(request, 'hr_management/admin/salary_slip_search.html', {'error_message': error_message, 'usernames': usernames})
    else:
        # Fetch distinct years and months from SalarySlip model
        distinct_years = SalarySlip.objects.values_list('year', flat=True).distinct()
        distinct_months = SalarySlip.objects.values_list('month', flat=True).distinct()
        usernames = CustomUser.objects.filter(Q(user_type=3) | Q(user_type=4)).values_list('username', flat=True).order_by('username')
        return render(request, 'hr_management/admin/salary_slip_search.html', {'usernames': usernames, 'distinct_years': distinct_years, 'distinct_months': distinct_months})


@login_required(login_url='do_login')
@require_user_type(user_type=[1,2])
def total_managers(request):
    try:
        managers = CustomUser.objects.filter(user_type=4)
        return render(request,'hr_management/admin/total_managers.html',{'managers':managers})
    except CustomUser.DoesNotExist:
        messages.error(request,"No Managers found")
    except BaseException as a:
        messages.error(request,f"An Error Occured {a}")


def send_reimbursement_reminder_email():
    print('send_reimbursement_reminder_email')
    try:
        reimb_bills = Reimbursement_bill.objects.filter(reimbursement_status=0)
        for reimb_bill in reimb_bills:
            employee = reimb_bill.employee_id
            manager_name = employee.admin.manager
            manager_email = CustomUser.objects.filter(username=manager_name).values_list('email', flat=True).first()
            if manager_email:
                email_subject = 'Reminder Approve Reimbursement'
                application_link = 'http://app1.olatechs.com:8080/'
                email_template = 'hr_management/admin/send_reimbursement_email.html'
                email_context = {
                    'employee_name': employee.admin.username,
                    'bill_no': reimb_bill.bill_no,
                    'manager_name': manager_name,
                    'date': reimb_bill.created_at,
                    'amount': reimb_bill.total_amount,
                    'reason': reimb_bill.query,
                    'description': reimb_bill.approved_by,
                    'application_link':application_link,
                }
                email_html_message = render_to_string(email_template, email_context)
                email_plain_message = strip_tags(email_html_message)
                from_email = f'{settings.EMAIL_FROM_NAME} <{getattr(settings, "EMAIL_HOST_USER", "default_from_email")}>'
                # from_email = getattr(settings, 'EMAIL_HOST_USER', 'default_from_email')
                send_mail(email_subject, email_plain_message, from_email, [manager_email], html_message=email_html_message)
    except Exception as e:
        print(e)


def send_reimbursement_reminder_email_account():
    print('send_reimbursement_reminder_email_account')
    try:
        reimb_bills = Reimbursement_bill.objects.filter(reimbursement_status=1)
        account_user = CustomUser.objects.filter(user_type=5).first() 
        for reimb_bill in reimb_bills:
            employee = reimb_bill.employee_id
            account_email = account_user.email

            if account_email:
                email_subject = 'Reminder Reimbursement Approval From Manager'
                application_link = 'http://app1.olatechs.com:8080/'
                email_template = 'hr_management/manager_template/send_account_reimbursement_email.html'
                email_context = {
                    'employee_name': employee.admin.username,
                    'bill_no': reimb_bill.bill_no,
                    'date': reimb_bill.created_at,
                    'amount': reimb_bill.total_amount,
                    'reason': reimb_bill.query,
                    'description': reimb_bill.approved_by,
                    'application_link':application_link
                }
                email_html_message = render_to_string(email_template, email_context)
                email_plain_message = strip_tags(email_html_message)
                from_email = f'{settings.EMAIL_FROM_NAME} <{getattr(settings, "EMAIL_HOST_USER", "default_from_email")}>'
                # from_email = getattr(settings, 'EMAIL_HOST_USER', 'default_from_email')
                send_mail(email_subject, email_plain_message, from_email, [account_email], html_message=email_html_message)
    except Exception as e:
            print(e)



def send_leave_reminder_email():
    print('send_leave_reminder_email')
    try:
        leave_reports = LeaveReportEmployee.objects.filter(leave_status=0)
        for leave_report in leave_reports:
            employee = leave_report.employee_id
            manager_name = employee.admin.manager
            manager_email = CustomUser.objects.filter(username=manager_name).values_list('email', flat=True).first()
            first_name = employee.admin.first_name
            last_name = employee.admin.last_name
            leave_start_date = leave_report.leave_start_date
            leave_end_date = leave_report.leave_end_date
            if manager_email:
                email_subject = "Reminder Approve Leave Application"
                application_link = 'http://app1.olatechs.com:8080/'
                email_template = 'hr_management/employee_template/send_email.html'
                email_context = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'leave_start_dates': leave_start_date,
                    'leave_end_dates': leave_end_date,
                    'application_link':application_link
                }
                email_html_message = render_to_string(email_template, email_context)
                email_plain_message = strip_tags(email_html_message)
                from_email = f'{settings.EMAIL_FROM_NAME} <{getattr(settings, "EMAIL_HOST_USER", "default_from_email")}>'
                send_mail(email_subject, email_plain_message, from_email, [manager_email], html_message=email_html_message)
    except Exception as e:
        print(e)




def schedule_email_sending():
    print('Scheduling leave email')
    send_leave_reminder_email()
    send_reimbursement_reminder_email_account()
    send_reimbursement_reminder_email()

# Call the function directly without threading
schedule_email_sending()
