import json
import requests
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from hr_management_app.EmailBackEnd import EmailBackEnd
from .models import *
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required


def ShowLoginPage(request):
    return render(request,"hr_management/login_page.html")

def doLogin(request):
        # captcha_token=request.POST.get("g-recaptcha-response")
        # cap_url="https://www.google.com/recaptcha/api/siteverify"
        # cap_secret="6LeWtqUZAAAAANlv3se4uw5WAg-p0X61CJjHPxKT"
        # cap_data={"secret":cap_secret,"response":captcha_token}
        # cap_server_response=requests.post(url=cap_url,data=cap_data)
        # cap_json=json.loads(cap_server_response.text)

        # if cap_json['success']==False:
        #     messages.error(request,"Invalid Captcha Try Again")
        #     return HttpResponseRedirect("/")
    

        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type=="2":
                return HttpResponseRedirect(("/hr_home"))
            elif user.user_type=="3":
                return HttpResponseRedirect(("/employee_home"))
            elif user.user_type=="4":
                return HttpResponseRedirect(("/manager_home"))
            elif user.user_type=="5":
                return HttpResponseRedirect(("/account_home"))
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

# def showFirebaseJS(request):
#     data='importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
#          'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
#          'var firebaseConfig = {' \
#          '        apiKey: "YOUR_API_KEY",' \
#          '        authDomain: "FIREBASE_AUTH_URL",' \
#          '        databaseURL: "FIREBASE_DATABASE_URL",' \
#          '        projectId: "FIREBASE_PROJECT_ID",' \
#          '        storageBucket: "FIREBASE_STORAGE_BUCKET_URL",' \
#          '        messagingSenderId: "FIREBASE_SENDER_ID",' \
#          '        appId: "FIREBASE_APP_ID",' \
#          '        measurementId: "FIREBASE_MEASUREMENT_ID"' \
#          ' };' \
#          'firebase.initializeApp(firebaseConfig);' \
#          'const messaging=firebase.messaging();' \
#          'messaging.setBackgroundMessageHandler(function (payload) {' \
#          '    console.log(payload);' \
#          '    const notification=JSON.parse(payload);' \
#          '    const notificationOption={' \
#          '        body:notification.body,' \
#          '        icon:notification.icon' \
#          '    };' \
#          '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
#          '});'

#     return HttpResponse(data,content_type="text/javascript")


def signup_admin(request):
    return render(request,"hr_management/signup_admin_page.html")


def signup_employee(request):
    employee=Employees.objects.all()
    return render(request,"hr_management/signup_employee_page.html",{"employee":employee})


def signup_hr(request):
    return render(request,"hr_management/signup_hr_page.html")

def signup_manager(request):
    return render(request,"hr_management/signup_manager_page.html")

def signup_account(request):
    return render(request,"hr_management/signup_account_page.html")

def do_signup_account(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    # Check if an employee with the same username or email already exists
    if CustomUser.objects.filter(Q(username=username) | Q(email=email)).exists():
        messages.error(request, "An Account with the same username or email already exists.")
        return HttpResponseRedirect(reverse("show_login"))

    try:
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            last_name=last_name,
            first_name=first_name,
            user_type=5
        )
        user.accounts.save()
        messages.success(request, "Successfully Added Account.")
        return HttpResponseRedirect(reverse("show_login"))
    except BaseException as e:
        messages.error(request, f"Failed to create Account: {str(e)}")
        return HttpResponseRedirect(reverse("show_login"))




def do_admin_signup(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")


    try:
        user=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password,email=email,user_type=1)
        user.save()
        messages.success(request,"Successfully Created Admin")
        return HttpResponseRedirect(reverse("show_login"))
    except BaseException as a:
        messages.error(request,"Failed to Create Admin")
        return HttpResponseRedirect(reverse("show_login"))

def do_hr_signup(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    try:
        user=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password,email=email,user_type=2)
        user.save()
        messages.success(request,"Successfully Created HR")
        return HttpResponseRedirect(reverse("show_login"))
    except BaseException as e:
        messages.error(request,"Failed to Create HR")
        return HttpResponseRedirect(reverse("show_login"))


def do_signup_employee(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    # Check if an employee with the same username or email already exists
    if CustomUser.objects.filter(Q(username=username) | Q(email=email)).exists():
        messages.error(request, "An employee with the same username or email already exists.")
        return HttpResponseRedirect(reverse("show_login"))

    try:
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            last_name=last_name,
            first_name=first_name,
            user_type=3
        )
        user.employees.save()

        messages.success(request, "Successfully added employee.")
        return HttpResponseRedirect(reverse("show_login"))
    except BaseException as e:
        messages.error(request, f"Failed to create employee: {str(e)}")
        return HttpResponseRedirect(reverse("show_login"))


    
def do_signup_manager(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    # Check if an employee with the same username or email already exists
    if CustomUser.objects.filter(Q(username=username) | Q(email=email)).exists():
        messages.error(request, "An manager with the same username or email already exists.")
        return HttpResponseRedirect(reverse("show_login"))

    try:
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            last_name=last_name,
            first_name=first_name,
            user_type=4
        )
        user.employees.save()
        messages.success(request, "Successfully added employee.")
        return HttpResponseRedirect(reverse("show_login"))
    except BaseException as e:
        messages.error(request, f"Failed to create manager: {str(e)}")
        return HttpResponseRedirect(reverse("show_login"))




User = get_user_model()

def reset_password(request):
    user_not_exist = False  # Initialize the variable

    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user_not_exist = True  # Set the variable to True if the user does not exist
        else:
            # Generate the password reset token
            token = default_token_generator.make_token(user)

            # Generate the password reset link
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri('/password_reset/{}/{}/'.format(uid, token))

            # Compose the email
            subject = 'Password Reset'
            message = render_to_string('hr_management/reset_password_email.html', {
                'user': user,
                'reset_link': reset_link
            })
            plain_text_message = strip_tags(message)
            # from_email = getattr(settings,'EMAIL_HOST_USER','default_from_email')
            from_email = f'{settings.EMAIL_FROM_NAME} <{getattr(settings, "EMAIL_HOST_USER", "default_from_email")}>'
            email = EmailMessage(subject, plain_text_message,from_email,to=[email])
            email.send()
            messages.success(request, 'Password reset email has been sent. Please check your inbox.')
            return redirect('show_login')
    return render(request, 'hr_management/reset_password.html', {'user_not_exist': user_not_exist})



def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('reset_password')

    if default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password == confirm_password:
                user.set_password(password)
                user.save()
                return redirect('do_login')
            else:
                messages.error(request, 'Passwords do not match. Please try again.')
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('reset_password')

    return render(request, 'hr_management/reset_password_confirm.html')


def custom_404_view(request, exception):
    return render(request, 'hr_management/404_not_found.html')