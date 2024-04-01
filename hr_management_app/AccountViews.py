from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from .decorators import require_user_type
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.shortcuts import render,render, get_object_or_404
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import os
import zipfile
from django.utils import timezone
from django.http import FileResponse
from datetime import datetime, timedelta
from django.core.files.storage import default_storage



@login_required(login_url='do_login')
@require_user_type(user_type=5)
def account_home(request):
    try:
        return render(request,"hr_management/account_template/home_content.html")
    except BaseException:
        messages.error(request, "May be something went to wrong")



@login_required(login_url='do_login')
@require_user_type(5)
def account_profile(request):
    try:
        user=CustomUser.objects.get(id=request.user.id)
        return render(request,"hr_management/account_template/account_profile.html",{"user":user})
    except BaseException as a:
        print(a)



@login_required(login_url='do_login')
@require_user_type(5)
def account_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("account_profile"))
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
            return HttpResponseRedirect(reverse("account_home"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("account_profile"))
        

@login_required(login_url='do_login')
@require_user_type(user_type=[1,5])
def reimbursement_history_view(request):
    try:
        # reimbursement = Reimbursement_bill.objects.filter(Q(reimbursement_status=1) | Q(reimbursement_status=3))
        reimbursement = Reimbursement_bill.objects.filter(Q(reimbursement_status=1) | Q(reimbursement_status=3)).order_by('-id')
        items_per_page = 10 
        paginator = Paginator(reimbursement, items_per_page)
        page_number = request.GET.get('page')
        try:
            paginated_reimbursement = paginator.get_page(page_number)
        except PageNotAnInteger:
            paginated_reimbursement = paginator.get_page(1)
        except EmptyPage:
            paginated_reimbursement = paginator.get_page(paginator.num_pages)
        template_name = 'hr_management/account_template/account_reimbursemenet.html'
        context = {'reimbursement': paginated_reimbursement}
        return render(request, template_name, context)
    except BaseException as a:
        print(a)
        
@login_required(login_url='do_login')
@require_user_type(user_type=[1,5])
def employee_approve_reimbursement_account(request, id):
    try:
        records = Reimbursement_bill.objects.filter(id=id)
        for record in records:
            employee_email = record.employee_id.admin.email
            first_name = record.employee_id.admin.first_name
            last_name = record.employee_id.admin.last_name
            employee_name = f'{first_name} {last_name}'
            bill_no = record.bill_no
            record.reimbursement_status = 3
            record.query = 'Approved by Accounts'
            record.save()
            account_send_reimbursement_approval_email(employee_email,bill_no,employee_name)
        if request.user.user_type == '5':
            return redirect('reimbursement_history_view')
        else:
            return redirect('manage_reimbursement_view')
    except BaseException as a:
        print(a)
         
def account_send_reimbursement_approval_email(employee_email,bill_no,employee_name):
    # Construct the email content
    email_subject = 'Reimbursement Approval From Account'
    application_link = 'http://app1.olatechs.com:8080/'
    email_template = 'hr_management/account_template/send_employee_reimbursement_email_account.html'  # Replace with the actual path
    email_context = {
        'bill_no': bill_no,
        "employee_name":employee_name,
        'application_link':application_link,
    }
    email_html_message = render_to_string(email_template, email_context)
    email_plain_message = strip_tags(email_html_message)
    from_email = f'{settings.EMAIL_FROM_NAME} <{getattr(settings, "EMAIL_HOST_USER", "default_from_email")}>'
    to_email = employee_email  # Replace with the recipient's email address
    send_mail(email_subject, email_plain_message, from_email, [to_email], html_message=email_html_message)


@login_required(login_url='do_login')
@require_user_type(user_type=[1,5])
def employee_disapprove_reimbursement_account(request, id):
    record = get_object_or_404(Reimbursement_bill, id=id)
    bill_no = record.bill_no
    employee_email = record.employee_id.admin.email
    first_name = record.employee_id.admin.first_name
    last_name = record.employee_id.admin.last_name
    employee_name = f'{first_name} {last_name}'
    if request.method == 'POST':
        query = request.POST.get('query')
        record.query = 'Rejected by Accounts:' + query 
        record.reimbursement_status = 2
        record.save()
        account_send_reimbursement_disapproval_email(employee_email,bill_no,employee_name)
    if request.user.user_type == '5':
        return redirect('reimbursement_history_view')
    else:
         return redirect('manage_reimbursement_view')


def account_send_reimbursement_disapproval_email(employee_email,bill_no,employee_name):
    # Construct the email content
    email_subject = 'Reimbursement Send Back From Accounts'
    application_link = 'http://app1.olatechs.com:8080/'
    email_template = 'hr_management/account_template/send_employee_reimbursement_email_account_reject.html'  # Replace with the actual path
    email_context = {
        'bill_no': bill_no,
        'employee_name':employee_name,
        'application_link':application_link
    }
    email_html_message = render_to_string(email_template, email_context)
    email_plain_message = strip_tags(email_html_message)
    from_email = f'{settings.EMAIL_FROM_NAME} <{getattr(settings, "EMAIL_HOST_USER", "default_from_email")}>'
    to_email = employee_email
    send_mail(email_subject, email_plain_message, from_email, [to_email], html_message=email_html_message)




@login_required(login_url='do_login')
@require_user_type(user_type=[1,5])
def download_reimbursement_files(request):
    if request.method == 'POST':
        try:
            selected_year = request.POST.get('year')
            selected_month = request.POST.get('month')
            if selected_year and selected_month:
                selected_year = int(selected_year)
                selected_month = int(selected_month)

                # Create start_date and end_date for the selected year and month
                start_date = datetime(selected_year, selected_month, 1)
                end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)

                reimbursement_data = Reimbursement_data.objects.filter(
                    bill_no__created_at__range=(start_date, end_date)
                )

                temp_dir = f"temp_reimbursement_{selected_year}_{selected_month}"
                os.makedirs(temp_dir, exist_ok=True)

                for file_data in reimbursement_data:
                    if file_data.attachment:
                        file_path = default_storage.url(file_data.attachment.name)
                        file_name = os.path.basename(file_path)
                        file_save_path = os.path.join(temp_dir, file_name)
                        with open(file_save_path, 'wb') as destination_file:
                            with default_storage.open(file_data.attachment.name, 'rb') as source_file:
                                destination_file.write(source_file.read())

                # Create a zip file containing the downloaded files
                zip_file_name = f"reimbursement_{selected_year}_{selected_month}.zip"
                with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, temp_dir)
                            zipf.write(file_path, arcname=arcname)

                # Clean up temporary directory
                for file_data in reimbursement_data:
                    if file_data.attachment:
                        file_path = default_storage.url(file_data.attachment.name)
                        file_name = os.path.basename(file_path)
                        file_save_path = os.path.join(temp_dir, file_name)
                        os.remove(file_save_path)
                os.rmdir(temp_dir)

                # Create a response to return the zip file for download
                response = FileResponse(open(zip_file_name, 'rb'), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename="{zip_file_name}"'
                return response
            else:
                pass
        except Exception as e:
            print(e)

    # Retrieve unique years and months for the dropdown menu
    month_names = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
        }

    created_at_values = Reimbursement_bill.objects.values('created_at')

    # Extract the month and year using Python and create separate lists
    months = [item['created_at'].month for item in created_at_values]
    years = [item['created_at'].year for item in created_at_values]

    # Get unique values for months and years
    unique_years = list(set(years))
    unique_months = list(set(months))

    context = {
        'years': unique_years,
        'months': unique_months,
    }
    if request.user.user_type == '5':
        return render(request, 'hr_management/account_template/download_reimbursement_files.html', context)
    else:
        return render(request, 'hr_management/admin/download_reimbursement_files.html', context)
