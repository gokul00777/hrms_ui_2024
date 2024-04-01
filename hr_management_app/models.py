from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta,datetime


class CustomUser(AbstractUser):
    user_type_data=((1,"Admin"),(2,"HR"),(3,"Employee"),(4,"Manager"),(5,'Account'))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)
    email = models.EmailField(unique=True)
    manager = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)  # Add this field for user activation
    def is_active_user(self):
        return self.is_active

class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Accounts(models.Model):
    id = models.AutoField(primary_key=True)
    created_at=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    objects = models.Manager()
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)


class HRs(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    department = models.CharField(max_length=50)
    manager = models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    fcm_token=models.TextField(default="")
    objects=models.Manager()


class Employees(models.Model):
    id = models.AutoField(primary_key=True)
    emp_id = models.CharField(max_length=25, blank=True)

    def save(self, *args, **kwargs):
        # set the emp_id field to the next available ID in the format OTS_XXXXX
        if not self.emp_id:
            last_emp = Employees.objects.order_by('-id').first()
            if last_emp:
                last_number = int(last_emp.emp_id.split('_')[1])
            else:
                last_number = 10000  # Start with 10000 if no previous employee exists
            self.emp_id = 'OTS_{:05d}'.format(last_number + 1)
        super(Employees, self).save(*args, **kwargs)

    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    profile_pic= models.FileField(null=True,blank=True)
    fcm_token = models.TextField(default="")
    objects = models.Manager()

################################# On Boarding ############################################
class Employee_Onboarding(models.Model):
    MARITAL_STATUS=(
        ('married','Married'),
        ('unmarried','Unmarried')
    )
    Gender = (
        ('male','Male'),
        ('female','Female'),
        ('other','Other')
    )
    employee=models.OneToOneField(Employees,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_no= models.CharField(max_length=10)
    emergency_contact_no = models.CharField(max_length=10)
    pancard_no= models.CharField(max_length=10,unique=True)
    adhaar_no= models.CharField(max_length=12,unique=True) 
    pf_uan_no = models.CharField(max_length=30,unique=True)
    blood_group = models.CharField(max_length=20)
    dob = models.DateField()
    gender = models.CharField(max_length=20,choices=Gender)
    marital_status = models.CharField(max_length=30, choices=MARITAL_STATUS)
    highest_qualification = models.CharField(max_length=50)
    previous_company_name = models.CharField(max_length=30)
    date_of_joining = models.DateField()


class Address_detail(models.Model):
    ADDRESS_TYPES = (
        ('current', 'Current Address'),
        ('permanent', 'Permanent Address'),
        ('other', 'Other Address'),
    )
    employee=models.OneToOneField(Employees,on_delete=models.CASCADE)
    add_type = models.CharField(max_length=30, choices=ADDRESS_TYPES, default='current')
    address1 = models.CharField(max_length=1024)
    address2 = models.CharField(max_length=1024)
    zip_code = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    dist = models.CharField(max_length=100)
    state = models.CharField(max_length=100,default='Maharashtra')
    country = models.CharField(max_length=30)
    
    def __str__(self):
        return f'{self.employee}'

class Permanent_Address(models.Model):
    ADDRESS_TYPES = (
        ('current', 'Current Address'),
        ('permanent', 'Permanent Address'),
        ('other', 'Other Address'),
    )
    employee=models.OneToOneField(Employees,on_delete=models.CASCADE)
    per_add_type = models.CharField(max_length=30, choices=ADDRESS_TYPES, default='perment')
    per_address1 = models.CharField(max_length=200)
    per_address2 = models.CharField(max_length=200)
    per_zip_code = models.CharField(max_length=6)
    per_city = models.CharField(max_length=100)
    per_dist = models.CharField(max_length=100)
    per_state = models.CharField(max_length=100,default='Maharashtra')
    per_country = models.CharField(max_length=30)
    def __str__(self):
        return f'{self.employee}'


class FamilyDetails(models.Model):
    employee = models.OneToOneField(Employees, on_delete=models.CASCADE)
    member1_name = models.CharField(max_length=50)
    merber1_dob = models.DateField()
    merber1_aadhar_no = models.CharField(max_length=12)
    relationship1 = models.CharField(max_length=50)
    member2_name = models.CharField(max_length=50)
    merber2_dob = models.DateField()
    merber2_aadhar_no = models.CharField(max_length=12)
    relationship2 = models.CharField(max_length=50)
    member3_name = models.CharField(max_length=50, blank=True, null=True)
    merber3_dob = models.DateField(blank=True, null=True)
    merber3_aadhar_no = models.CharField(max_length=12, blank=True, null=True)
    relationship3 = models.CharField(max_length=50, blank=True, null=True)
    member4_name = models.CharField(max_length=50, blank=True, null=True)
    merber4_dob = models.DateField(null=True, blank=True)
    merber4_aadhar_no = models.CharField(max_length=12, blank=True, null=True)
    relationship4 = models.CharField(max_length=50, blank=True, null=True)
    member5_name = models.CharField(max_length=50, blank=True, null=True)
    merber5_dob = models.DateField(null=True, blank=True)
    merber5_aadhar_no = models.CharField(max_length=12, blank=True, null=True)
    relationship5 = models.CharField(max_length=50, blank=True, null=True)


class BankDetails(models.Model):
    employee=models.OneToOneField(Employees,on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    account_number = models.CharField(max_length=20)
    ifsc_number = models.CharField(max_length=20)


def get_upload_to(instance, filename):
    return "pdfs/employee_{id}/{filename}".format(id=instance.employee.id, filename=filename)

class Documents(models.Model):
    employee = models.OneToOneField(Employees, on_delete=models.CASCADE)
    employee_photo = models.FileField(upload_to=get_upload_to)
    employee_aadhar = models.FileField(upload_to=get_upload_to)
    employee_pan = models.FileField(upload_to=get_upload_to)
    ssc_marksheet = models.FileField(upload_to=get_upload_to)
    hsc_marksheet = models.FileField(upload_to=get_upload_to, null=True,blank=True)
    diploma_marksheet = models.FileField(upload_to=get_upload_to, null=True,blank=True)
    degree_marksheet = models.FileField(upload_to=get_upload_to)
    bank_passbook = models.FileField(upload_to=get_upload_to)
    passport = models.FileField(upload_to=get_upload_to,null=True,blank=True)
    reliving_letter = models.FileField(upload_to=get_upload_to)
    family_member1_aadhar = models.FileField(upload_to=get_upload_to)
    family_member2_aadhar = models.FileField(upload_to=get_upload_to)
    family_member3_aadhar = models.FileField(upload_to=get_upload_to,blank=True, null=True)
    family_member4_aadhar = models.FileField(upload_to=get_upload_to,blank=True, null=True)
    family_member5_aadhar = models.FileField(upload_to=get_upload_to,blank=True, null=True)



class LeaveReportEmployee(models.Model):
    id=models.AutoField(primary_key=True)
    employee_id=models.ForeignKey(Employees,on_delete=models.CASCADE)
    leave_date=models.DateTimeField(max_length=255, null=True,blank=True)
    leave_message=models.TextField()
    leave_status=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    leave_type=models.CharField(max_length=100)
    leave_start_date = models.DateField(max_length=255)
    leave_end_date = models.DateField(max_length=255)
    def leave_dates(self):
        return [self.leave_start_date + timedelta(days=i) for i in range((self.leave_end_date - self.leave_start_date).days + 1)]


class EmployeeLeave(models.Model):
    id=models.AutoField(primary_key=True)
    employee_id=models.ForeignKey(Employees,on_delete=models.CASCADE)
    EarnLeave =models.FloatField(default=0)
    CasualLeave =models.FloatField(default=0)
    TotalLeaves = models.FloatField(default=0)
    EarnLeave_used =models.FloatField(default=0)
    CasualLeave_used =models.FloatField(default=0)
    month_updated = models.IntegerField(default=0)
    year_updated = models.IntegerField(default=0)
    Prev_CFEL = models.FloatField(default=0)
    current_EL = models.FloatField(default=0)
    code_executed = models.BooleanField(default=False)
    else_executed=models.BooleanField(default=False)

 



class LeaveReportHR(models.Model):
    id = models.AutoField(primary_key=True)
    hr_id = models.ForeignKey(HRs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackEmployee(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackHRs(models.Model):
    id = models.AutoField(primary_key=True)
    hr_id = models.ForeignKey(HRs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationEmployee(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationHRs(models.Model):
    id = models.AutoField(primary_key=True)
    hr_id = models.ForeignKey(HRs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()




@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        elif instance.user_type==2:
            HRs.objects.create(admin=instance)
        elif instance.user_type==3 or instance.user_type==4:
            Employees.objects.create(admin=instance)
        elif instance.user_type==5:
            Accounts.objects.create(admin=instance)


@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    elif instance.user_type==2:
        instance.hrs.save()
    elif instance.user_type == 3 or instance.user_type == 4:
        instance.employees.save()
    elif instance.user_type == 5:
        instance.accounts.save()
    



######################### OFFER LETTER ########################################
class OfferLetter(models.Model):
    basic_pay = models.DecimalField(max_digits=10, decimal_places=2)
    total_fixed_pay = models.DecimalField(max_digits=10, decimal_places=2)
    total_variable_pay = models.DecimalField(max_digits=10, decimal_places=2)
    insurance_premiums = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost_to_company = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    esic = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    employer_pf_contribution = models.DecimalField(max_digits=10, decimal_places=2)
    flexible_components_tfp = models.DecimalField(max_digits=10, decimal_places=2)

class OfferLetter_Sended(models.Model):
    offerletter = models.OneToOneField(OfferLetter,on_delete=models.CASCADE)
    ctc = models.FloatField()
    name = models.CharField(max_length=100)
    offer_release_date = models.DateField()
    joining_date = models.DateField()
    address = models.CharField(max_length=100)
    designation = models.CharField(max_length=50)
    job_grade = models.IntegerField()
    reporting = models.CharField(max_length=50)
    hr_name = models.CharField(max_length=50)
    offer_accept_date = models.DateField()
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=50)


    


class WageRegister(models.Model):
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE, related_name='wage_registers')
    ctc = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    esic = models.DecimalField(max_digits=10, decimal_places=2)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    flexible_component = models.DecimalField(max_digits=10, decimal_places=2)
    variable_component = models.DecimalField(max_digits=10, decimal_places=2)
    provident_fund = models.DecimalField(max_digits=10, decimal_places=2)
    professional_tax = models.DecimalField(max_digits=10, decimal_places=2)
    income_tax = models.DecimalField(max_digits=10, decimal_places=2,default='00')
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    other_allowns = models.DecimalField(max_digits=10,decimal_places=2,default='00')
    lwf = models.DecimalField(max_digits=10,decimal_places=2,default='00')

    

    # YTD fields
    ytd_ctc = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_hra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_esic = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_flexible_component = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_variable_component = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_provident_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_professional_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_income_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_gross_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_total_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Additional fields
    days_payable = models.IntegerField()
    days_paid = models.IntegerField(null=True)
    address = models.CharField(max_length=500)
    month = models.CharField(max_length=30)
    year = models.CharField(max_length=30) 
    age = models.CharField(max_length=20) 
    sunday_and_holidays = models.CharField(max_length=40)
    new_days_payable = models.CharField(max_length=40)



class SalarySlip(models.Model):
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE, related_name='salary_slips')
    ctc = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    esic = models.DecimalField(max_digits=10, decimal_places=2)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    flexible_component = models.DecimalField(max_digits=10, decimal_places=2)
    variable_component = models.DecimalField(max_digits=10, decimal_places=2)
    provident_fund = models.DecimalField(max_digits=10, decimal_places=2)
    professional_tax = models.DecimalField(max_digits=10, decimal_places=2)
    income_tax = models.DecimalField(max_digits=10, decimal_places=2,default='00')
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    other_allowns = models.DecimalField(max_digits=10,decimal_places=2,default='00')
    lwf = models.DecimalField(max_digits=10,decimal_places=2,default='00')

    

    # YTD fields
    ytd_ctc = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_hra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_esic = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_flexible_component = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_variable_component = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_provident_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_professional_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_income_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_gross_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_total_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ytd_net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Additional fields
    days_payable = models.IntegerField()
    days_paid = models.IntegerField(null=True)
    address = models.CharField(max_length=500)
    month = models.CharField(max_length=30)
    year = models.CharField(max_length=30)


def get_upload(instance, filename):
    first_name = instance.employee_id.admin.first_name
    last_name = instance.employee_id.admin.last_name
    emp_id = instance.employee_id.emp_id
    sr_no = instance.sr_no
    amount = instance.amount
    reimbursement_bill = instance.bill_no 
    bill_no = reimbursement_bill.bill_no
    current_date = datetime.now()
    year_month = current_date.strftime("%Y-%m")
    new_filename = f"{first_name}_{last_name}_{emp_id}_{bill_no}_{sr_no}_{amount}_{current_date.strftime('%Y-%m-%d')}"
    ext = filename.split('.')[-1]
    return f"reimbursements/{year_month}/{first_name}_{last_name}/{new_filename}.{ext}"

    
class Reimbursement_bill(models.Model):
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE, related_name='reimbursement_bill')
    bill_no = models.IntegerField()
    reimbursement_status=models.IntegerField(default=0,blank=True,null=True)
    query = models.TextField(max_length=100, blank=True, null=True, default='')
    approved_by = models.TextField(max_length=100, blank=True, default='')
    # approved_by_account = models.TextField(max_length=100, blank=True, default='')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    


class Reimbursement_data(models.Model):
    Reason = (
        ('','Select'),
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Sales Incentive','Sales Incentive'),
        ('Other', 'Other'),
    )
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    bill_no = models.ForeignKey(Reimbursement_bill, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    amount = models.IntegerField(null=True)
    reason = models.CharField(max_length=50,choices=Reason,null=True)
    attachment = models.FileField(upload_to=get_upload,null=True)
    sr_no = models.CharField(max_length=50,null=True)
    description =  models.CharField(max_length=250,null=True)
    





