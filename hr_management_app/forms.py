from django import forms
from django.forms import ChoiceField
from .models import *
from django.core.exceptions import ValidationError
from hr_management_app.models import *
import re

class ChoiceNoValidation(ChoiceField):
    def validate(self, value):
        pass

class DateInput(forms.DateInput):
    input_type = "date"

class EmployeeOnboardingForm(forms.ModelForm):
    class Meta:
        model = Employee_Onboarding
        exclude =['employee']
        labels = {
            'contact_no': 'Contact Number',
            'emergency_contact_no': 'Emergency Contact Number',
            'pancard_no': 'PAN Card Number',
            'adhaar_no': 'Aadhaar Card Number',
            'pf_uan_no': 'PF UAN Number',
            'blood_group': 'Blood Group',
            'dob': 'Date of Birth',
            'gender':'Gender',
            'marital_status': 'Marital Status',
            'highest_qualification': 'Highest Qualification',
            'previous_company_name': 'Previous Company Name',
            'date_of_joining': 'Date of Joining',
        }

        widgets = {
            'contact_no': forms.TextInput(attrs={"class":"form-control"}),
            'emergency_contact_no': forms.TextInput(attrs={"class":"form-control"}),
            'pancard_no': forms.TextInput(attrs={"class":"form-control"}),
            'adhaar_no': forms.TextInput(attrs={"class":"form-control"}),
            'pf_uan_no': forms.TextInput(attrs={"class":"form-control"}),
            'blood_group': forms.TextInput(attrs={"class":"form-control"}),
            'dob': forms.DateInput(attrs={"class":"form-control", "type":"date"}),
            'gender': forms.Select(attrs={"class":"form-control"}),
            'marital_status': forms.Select(attrs={"class":"form-control"}),
            'highest_qualification': forms.TextInput(attrs={"class":"form-control"}),
            'previous_company_name': forms.TextInput(attrs={"class":"form-control"}),
            'date_of_joining': forms.DateInput(attrs={"class":"form-control", "type":"date"}),
        }
    
class EmployeeAddressDetailsFrom(forms.ModelForm):
    class Meta:
        model = Address_detail
        exclude = ['employee']
        labels = {
            'add_type': ' Address Type',
            'address1': 'Address Line 1',
            'address2': 'Address Line 2',
            'zip_code': 'Zip Code',
            'city': 'City',
            'dist': 'District',
            'state': 'State',
            'country': 'Country',
        }
        widgets = {
            'add_type': forms.Select(attrs={"class": "form-control"}),
            'address1': forms.TextInput(attrs={"class": "form-control"}),
            'address2': forms.TextInput(attrs={"class": "form-control"}),
            'zip_code': forms.TextInput(attrs={"class": "form-control"}),
            'city': forms.TextInput(attrs={"class": "form-control"}),
            'dist': forms.TextInput(attrs={"class": "form-control"}),
            'state': forms.TextInput(attrs={"class": "form-control"}),
            'country': forms.TextInput(attrs={"class": "form-control"}),
        }
  

class EmployeePermentAddressFrom(forms.ModelForm):
    class Meta:
        model = Permanent_Address
        exclude = ['employee']
        labels = {
            'per_add_type': 'Address Type',
            'per_address1': 'Address Line 1',
            'per_address2': 'Address Line 2',
            'per_zip_code': 'Zip Code',
            'per_city': 'City',
            'per_dist': 'District',
            'per_state': 'State',
            'per_country': 'Country',
        }
        widgets = {
            'per_add_type': forms.Select(attrs={"class": "form-control"}),
            'per_address1': forms.TextInput(attrs={"class": "form-control"}),
            'per_address2': forms.TextInput(attrs={"class": "form-control"}),
            'per_zip_code': forms.TextInput(attrs={"class": "form-control"}),
            'per_city': forms.TextInput(attrs={"class": "form-control"}),
            'per_dist': forms.TextInput(attrs={"class": "form-control"}),
            'per_state': forms.TextInput(attrs={"class": "form-control"}),
            'per_country': forms.TextInput(attrs={"class": "form-control"}),
        }

class FamilyDetailsForm(forms.ModelForm):
    class Meta:
        model = FamilyDetails
        exclude=['employee']
        labels = {
            'member1_name': 'Member1 Name',
            'merber1_dob': 'Member1 Date of Birth',
            'merber1_aadhar_no': 'Member1 Aadhar No',
            'relationship1': 'Relationship with Member1',
            'member2_name': 'Member2 Name',
            'merber2_dob': 'Member2 Date of Birth',
            'merber2_aadhar_no': 'Member2 Aadhar No',
            'relationship2': 'Relationship with Member2',
            'member3_name': 'Member 3 Name',
            'merber3_dob': 'Member3 Date of Birth',
            'merber3_aadhar_no': 'Member3 Aadhar No',
            'relationship3': 'Relationship with Member3',
            'member4_name': 'Member 4 Name',
            'merber4_dob': 'Member4 Date of Birth',
            'merber4_aadhar_no': 'Member4 Aadhar No',
            'relationship4': 'Relationship with Member4',
            'member5_name': 'Member 5 Name',
            'merber5_dob': 'Member5 Date of Birth',
            'merber5_aadhar_no': 'Member5 Aadhar No',
            'relationship5': 'Relationship with Member5',
}
        widgets = {
            'member1_name': forms.TextInput(attrs={"class": "form-control"}),
            'merber1_dob': forms.DateInput(attrs={"class": "form-control", "type":"date"}),
            'merber1_aadhar_no': forms.TextInput(attrs={"class": "form-control"}),
            'relationship1': forms.TextInput(attrs={"class": "form-control"}),
            'member2_name': forms.TextInput(attrs={"class": "form-control"}),
            'merber2_dob': forms.DateInput(attrs={"class": "form-control", "type":"date"}),
            'merber2_aadhar_no': forms.TextInput(attrs={"class": "form-control"}),
            'relationship2': forms.TextInput(attrs={"class": "form-control"}),
            'member3_name': forms.TextInput(attrs={"class": "form-control"}),
            'merber3_dob': forms.DateInput(attrs={"class": "form-control", "type":"date"}),
            'merber3_aadhar_no': forms.TextInput(attrs={"class": "form-control"}),
            'relationship3': forms.TextInput(attrs={"class": "form-control"}),
            'member4_name': forms.TextInput(attrs={"class": "form-control"}),
            'merber4_dob': forms.DateInput(attrs={"class": "form-control", "type":"date"}),
            'merber4_aadhar_no': forms.TextInput(attrs={"class": "form-control"}),
            'relationship4': forms.TextInput(attrs={"class": "form-control"}),
            'member5_name': forms.TextInput(attrs={"class": "form-control"}),
            'merber5_dob': forms.DateInput(attrs={"class": "form-control", "type":"date"}),
            'merber5_aadhar_no': forms.TextInput(attrs={"class": "form-control"}),
            'relationship5': forms.TextInput(attrs={"class": "form-control"}),

        }



class BankDetailsForm(forms.ModelForm):
    class Meta:
        model = BankDetails
        exclude=['employee']
        labels={
            'bank_name':'Bank Name',
            'branch':'Branch Name',
            'account_number':'Account Number',
            'ifsc_number':'IFSC Number'
        }
        widgets ={
            'bank_name': forms.TextInput(attrs={'class':'form-control'}),
            'branch':forms.TextInput(attrs={"class": "form-control"}),
            'account_number':forms.TextInput(attrs={"class": "form-control"}),
            'ifsc_number':forms.TextInput(attrs={"class": "form-control"}),
        }

class DocumentsForm(forms.ModelForm):
    class Meta:
        model = Documents
        exclude=['employee']
        labels = {
            'employee_photo': 'Employee Photo',
            'employee_aadhar': 'Employee Aadhar',
            'employee_pan' : 'Employee PAN',
            'ssc_marksheet': 'SSC Marksheet',
            'hsc_marksheet': 'HSC Marksheet',
            'diploma_marksheet': 'Diploma Marksheet',
            'degree_marksheet': 'Degree Marksheet',
            'bank_passbook': 'Bank Passbook',
            'passport': 'Passport',
            'reliving_letter': 'Relieving Letter',
            'family_member1_aadhar': 'Family Member 1 Aadhar', 
            'family_member2_aadhar': 'Family Member 2 Aadhar', 
            'family_member3_aadhar': 'Family Member 3 Aadhar',
            'family_member4_aadhar': 'Family Member 4 Aadhar', 
            'family_member5_aadhar': 'Family Member 5 Aadhar',  
        }
        widgets= {
            'employee_photo':forms.FileInput(attrs={'class':'form-control'}),
            'employee_aadhar':forms.FileInput(attrs={'class':'form-control'}),
            'employee_pan' :forms.FileInput(attrs={'class':'form-control'}),
            'ssc_marksheet':forms.FileInput(attrs={'class':'form-control'}),
            'hsc_marksheet':forms.FileInput(attrs={'class':'form-control'}),
            'diploma_marksheet':forms.FileInput(attrs={'class':'form-control'}),
            'degree_marksheet':forms.FileInput(attrs={'class':'form-control'}),
            'bank_passbook':forms.FileInput(attrs={'class':'form-control'}),
            'passport':forms.FileInput(attrs={'class':'form-control'}),
            'reliving_letter':forms.FileInput(attrs={'class':'form-control'}),
            'family_member1_aadhar':forms.FileInput(attrs={'class':'form-control'}), 
            'family_member2_aadhar':forms.FileInput(attrs={'class':'form-control'}), 
            'family_member3_aadhar':forms.FileInput(attrs={'class':'form-control'}), 
            'family_member4_aadhar':forms.FileInput(attrs={'class':'form-control'}), 
            'family_member5_aadhar':forms.FileInput(attrs={'class':'form-control'}), 

        }






