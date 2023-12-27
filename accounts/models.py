from email.policy import default
from random import choices
from django.db import models
year_choices=((1,1),(2,2),(3,3))
department_choices=(("Automobile","Automobile"),("CS","CS"),("E and C","E and C"),("E and E","E and E"),("Civil","Civil"),("Mech","Mech"),("Dummy","Dummy"))
category_choices=(('SC/ST','SC/ST'),('SNQ','SNQ'),('Others','Others'))
sub_category_choices=(('--','--'),('2a','2a'),('2b','2b'),('3a','3a'),('3b','3b'),('cat-1','cat-1'))
class Student(models.Model):
    roll_no=models.CharField(max_length=15,primary_key=True)
    roll_no2=models.CharField(max_length=15,unique=True,null=True)
    admission_year=models.IntegerField(default=2023)
    name=models.CharField(max_length=30)
    gender=models.CharField(max_length=2,default="M",choices=(('M','M'),('F','F')))
    dep=models.CharField(max_length=20,choices=department_choices)
    category=models.CharField(max_length=20,choices=category_choices,default="Others")
    sub_category=models.CharField(max_length=20,choices=sub_category_choices,default="--")
    student_phone_number=models.CharField(max_length=20,default="12345")
    parent_name=models.CharField(max_length=30,default="abcde")
    parent_phone_number=models.CharField(max_length=20,default="12345")
    student_image=models.FileField(default="default.jpg")
    application_number=models.CharField(max_length=20,default="000000000")
    cancel_admission=models.BooleanField(default=False)
    year_completed=models.IntegerField(default=0)
    def __str__(self):
        return self.roll_no2

class Academic_Year(models.Model):
    academic_year=models.CharField(max_length=7,primary_key=True)
    def __str__(self):
        return self.academic_year

class Fees_Details(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    year=models.IntegerField(default=1,choices=year_choices)
    academic_year=models.ForeignKey(Academic_Year,on_delete=models.CASCADE)
    total_fees=models.IntegerField(default=0)
    collection=models.IntegerField(default=0)
    balance=models.IntegerField(default=0)
    def __str__(self):
        return self.student.roll_no+" "+str(self.year)

class History(models.Model):
    fees_receipt_no=models.CharField(primary_key=True,max_length=10)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    year=models.IntegerField(default=0) 
    academic_year=models.CharField(max_length=7)
    total_fees=models.IntegerField(default=0)
    tution_fees=models.IntegerField(default=0)
    admission_fees=models.IntegerField(default=0)
    id_fees=models.IntegerField(default=0)
    management_fees=models.IntegerField(default=0)
    lib_fees=models.IntegerField(default=0)
    assn_fees=models.IntegerField(default=0)
    rr_fees=models.IntegerField(default=0)
    swf_fees=models.IntegerField(default=0)
    twf_fees=models.IntegerField(default=0)
    lab_fees=models.IntegerField(default=0)
    sp_fees=models.IntegerField(default=0)
    nss_fees=models.IntegerField(default=0)
    dev_fees=models.IntegerField(default=0)
    date=models.DateField()
    def __str__(self):
        return str(self.fees_receipt_no)
    
class Application_Fees(models.Model):
    name=models.CharField(max_length=50)
    amount=models.IntegerField(default=0)
    academic_year=models.ForeignKey(Academic_Year,on_delete=models.CASCADE)
    fees_receipt_no=models.CharField(max_length=10,primary_key=True)
    
class Date(models.Model):
    name=models.CharField(primary_key=True,max_length=10)
    date=models.DateField() 
    def __str__(self) -> str:
        return self.name
    
    
    
# Create your models here.
