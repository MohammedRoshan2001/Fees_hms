from email.policy import default
from random import choices
from django.db import models
year_choices=((1,1),(2,2),(3,3))
department_choices=(("Automobile","Automobile"),("Computer Science","Computer Science"),("E and C","E and C"),("E and E","E and E"),("Civil","Civil"),("Mechanical","Mechanical"),("Dummy","Dummy"))
category_choices=(('SC','SC'),('SNQ','SNQ'),('Others','Others'),('ST','ST'))
sub_category_choices=(('--','--'),('2a','2a'),('2b','2b'),('3a','3a'),('3b','3b'),('cat-1','cat-1'),('GM','GM'),('SC','SC'),('ST',"ST"))
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
    merit_no = models.CharField(max_length=20, default="NA")
    Is_lateral = models.BooleanField(default=False)
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
    repeater=models.BooleanField(default= False)
    is_detained=models.BooleanField(default= False)
    def __str__(self):
        return self.student.roll_no2+"_"+str(self.year)+"_"+self.academic_year.academic_year

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
    
class Fees_Structure(models.Model):
    year=models.IntegerField(default=1,choices=year_choices)
    academic_year=models.ForeignKey(Academic_Year,on_delete=models.CASCADE)
    category=models.CharField(max_length=20,choices=category_choices,default="Others")
    repeater=models.BooleanField(default= False)
    is_lateral = models.BooleanField(default=False)
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
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['year', 'academic_year', 'category', 'repeater', 'is_lateral'],
                name='unique_fee_structure_combination'
            )
        ]
    def __str__(self) -> str:
        return str(self.year)+'_'+str(self.academic_year.academic_year)+"_"+self.category+'_'+str(self.repeater)+"_"+str(self.is_lateral)


class Detentions(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    year=models.IntegerField(default=1,choices=year_choices)
    academic_year=models.ForeignKey(Academic_Year,on_delete=models.CASCADE)
    is_detention_removed=models.BooleanField(default=False)

    
    
    
# Create your models here.
