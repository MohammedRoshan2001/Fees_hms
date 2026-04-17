
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from accounts.models import *
from datetime import datetime
from .forms import *
import openpyxl

from django.http import HttpResponse
from django.views.generic import View
 
#importing get_template from loader
from django.template.loader import get_template
 
#import render_to_pdf from util.py 

class Abst:
    def __init__(self,sl_no,dept,year,demand,collection,balance,count):
        self.sl_no=sl_no 
        self.dept=dept 
        self.year=year
        self.demand=demand 
        self.collection=collection 
        self.balance=balance 
        self.count=count
#Creating our view, it is a class based view 
class Collection:
    def __init__(self,receipt_no,date,fees) -> None:
        self.receipt_no=receipt_no 
        self.date=date 
        self.fees=fees
        pass
class Fees_Collection:
    def __init__(self,student,history) -> None:
        self.student=student 
        self.history=history
        pass

class Sub_Category:
    def __init__(self,name,count) -> None:
        self.name = name
        self.count = count
        pass

 
def reciept(request):
    return render(request,'print_reciept.html')
    pass

 
def add_data(request):
    if request.method == 'POST':
        excel_file = request.FILES["myfile"]
        print(excel_file)
        wb = openpyxl.load_workbook(excel_file)
        worksheet = wb["1"]
        print(worksheet)
        c = 0

        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value).strip())
            print(row_data)
            c += 1
            if c >= 2:
                st = History()
                student = Student.objects.get(roll_no=row_data[0])
                st.student = student
                st.fees_receipt_no =row_data[4]
                st.year = int(row_data[1])
                st.academic_year = row_data[2]
                st.total_fees= int(row_data[5])
                st.tution_fees = int(row_data[6])
                st.admission_fees = int(row_data[7])
                st.id_fees= int(row_data[8])
                st.management_fees = int(row_data[9])
                st.lib_fees= int(row_data[10])
                st.assn_fees = int(row_data[11])
                st.rr_fees = int(row_data[12])
                st.swf_fees = int(row_data[13])
                st.twf_fees = int(row_data[14])
                st.lab_fees = int(row_data[15])
                st.sp_fees = int(row_data[16])
                st.nss_fees = int(row_data[17])
                st.dev_fees = int(row_data[18])
                st.date =row_data[3][:10]
               
                st.save()
            
    return render(request, 'add_data.html')

def updating(request):
    s= {'CS':'Computer Science','Mech':'Mechanical'}
    for i in Student.objects.all():
        if i.dep in s:
            i.dep = s[i.dep]
            i.save()

    return HttpResponse('Success')


def index(request):
    print(len(Fees_Details.objects.all()))
    print(Fees_Details.objects.filter(student__roll_no='Prajwal'))

    s = {}
    
    for i in Fees_Details.objects.all():
        if i.student.category!= 'SNQ':
            if i.student.roll_no2 in s and i.total_fees == 6998:
                i.total_fees = 6848
                i.save()
                s[i.student.roll_no2].append((i,i.total_fees))
            else:
                s[i.student.roll_no2] = [(i,i.total_fees)]
    for i in s:
        if len(s[i])>1:
            print(s[i])
    print()
    return render(request, 'base.html')



def add_student(request):
    if request.method=="POST":
        usn=request.POST.get('usn')
        year=request.POST.get('year')
        repeater = request.POST.get('repeater')
        print(repeater, type(repeater))
        st=Student.objects.get(roll_no2=usn)
        y=int(year)
        rep = False
        if repeater == "1":
            rep = True

        student_objects=Fees_Details.objects.filter(student=st,year=y)
        if rep == True and len(student_objects) ==0:
            print('hi')
            return HttpResponse('<h1> Given Student is not a Repeater </h1>') 
        if rep == False and len(student_objects) ==1:
            return render(request,'student_exist.html')
        if len(student_objects) == 2:
            return HttpResponse('<h1> Maximum attempts completed for the given year </h1>')
            
        years_completed = 0
        for i in Fees_Details.objects.filter(student = st):
            years_completed = max(years_completed,i.year)
            
        if rep == True:
            years_completed -=1

        total_fee=-1
        if st.category=='SNQ':
                total_fee=1370
        elif years_completed==0:
            
            total_fee=6998
        else:
            total_fee=6848
            
            
        academic_year1=request.POST.get('academic_year')
        academic_year=Academic_Year.objects.get(academic_year=academic_year1)
    
        fees_obj=Fees_Details(student=st,year=y,repeater = rep,academic_year=academic_year,total_fees=total_fee,balance=total_fee)
        fees_obj.save()
        return HttpResponseRedirect(reverse('success'))
    else:
        student_list=Student.objects.all()
        year_list=Academic_Year.objects.all()
        context={'student_list':student_list,'year_list':year_list[::-1]}
        return render(request,'add_student.html',context)
    pass


def fees_updation(request):
    total, collection, balance, count = 0, 0, 0, 0

    # Default filter values
    academic_year = ""
    dept = ""
    year = ""
    reg_no = ""
    bal = None  # Checkbox for 'Only Balance'
    is_lateral = False  # Checkbox for 'Display Lateral'
    display_alphabetically = False

    if request.method == "POST":
        # Fetch form data from POST request
        dept = request.POST.get('dept', "---")
        year = request.POST.get('year', "---")
        academic_year = request.POST.get('academic_year', "---")
        reg_no = request.POST.get('reg_no', "").strip().upper()
        bal = request.POST.get('bal')  # Checkbox for 'Only Balance'
        is_lateral = request.POST.get('is_lateral') == '1'
        display_alphabetically = request.POST.get('display_alphabetically') == '1'

        # Set year filter
        year_filter = -1 if year == "---" else int(year)

        # Query all fee details based on filters
        student_list = []
        fees_qs = Fees_Details.objects.filter(student__cancel_admission=False)

        # Apply filters based on POST data
        if dept != "---":
            fees_qs = fees_qs.filter(student__dep=dept)

        if year_filter != -1:
            fees_qs = fees_qs.filter(year=year_filter)

        if academic_year != "---":
            fees_qs = fees_qs.filter(academic_year__academic_year=academic_year)

        if reg_no:
            fees_qs = fees_qs.filter(student__roll_no2__iexact=reg_no)  # Case-insensitive match

        if bal:
            fees_qs = fees_qs.filter(balance__gt=0)

        if is_lateral:
            fees_qs = fees_qs.filter(student__Is_lateral=True)

        # Process the filtered queryset
        for i in fees_qs:
            total += i.total_fees
            collection += i.collection
            balance += i.balance
            count += 1

            # Fetch payment history for the student
            history = [
                Collection(j.fees_receipt_no, j.date, j.total_fees)
                for j in History.objects.filter(student=i.student, year=i.year,academic_year=i.academic_year)
            ]
            student_list.append(Fees_Collection(i, history))

        # Sort the student list alphabetically if required
        if display_alphabetically:
            student_list.sort(key=lambda x: x.student.student.name)
        else:
            student_list = student_list[::-1]

        year_list = Academic_Year.objects.all()
        dep_list = department_choices

        context = {
            'student_list': student_list,
            'year_list': year_list[::-1],
            'dep_list': dep_list,
            'total': total,
            'collection': collection,
            'balance': balance,
            'dept': dept,
            'only_balance': bal,
            'academic_year': academic_year,
            'reg_no': reg_no,
            'year': year,
            'is_lateral': is_lateral,
            'display_alphabetically': display_alphabetically,
        }
        return render(request, 'fees_updation.html', context)

    # Default GET request handling
    student_list = []
    for i in Fees_Details.objects.filter(student__cancel_admission=False):
        total += i.total_fees
        collection += i.collection
        balance += i.balance
        count += 1

        history = [
            Collection(j.fees_receipt_no, j.date, j.total_fees)
            for j in History.objects.filter(student=i.student, year=i.year,academic_year=i.academic_year)
        ]
        student_list.append(Fees_Collection(i, history))

    year_list = Academic_Year.objects.all()
    dep_list = department_choices

    context = {
        'student_list': student_list[::-1],
        'year_list': year_list[::-1],
        'dep_list': dep_list,
        'total': total,
        'collection': collection,
        'balance': balance,
        'dept': "",
        'only_balance': "",
        'academic_year': "",
        'reg_no': "",
        'year': "",
        'is_lateral': False,
        'display_alphabetically': False,
    }
    return render(request, 'fees_updation.html', context)
    pass

def fees_updation_summary(request):
    total, collection, balance, count = 0, 0, 0, 0

    # Default filter values
    academic_year = ""
    dept = ""
    year = ""
    reg_no = ""
    bal = None  # Checkbox for 'Only Balance'
    is_lateral = False  # Checkbox for 'Display Lateral'
    display_alphabetically = False

    if request.method == "POST":
        # Fetch form data from POST request
        dept = request.POST.get('dept', "---")
        year = request.POST.get('year', "---")
        academic_year = request.POST.get('academic_year', "---")
        reg_no = request.POST.get('reg_no', "").strip().upper()
        bal = request.POST.get('bal')  # Checkbox for 'Only Balance'
        is_lateral = request.POST.get('is_lateral') == '1'
        is_snq = request.POST.get('is_snq') == '1'
        display_alphabetically = request.POST.get('display_alphabetically') == '1'

        # Set year filter
        year_filter = -1 if year == "---" else int(year)

        # Query all fee details based on filters
        student_list = []
        fees_qs = Fees_Details.objects.filter(student__cancel_admission=False).exclude(year=0)

        # Apply filters based on POST data
        if dept != "---":
            fees_qs = fees_qs.filter(student__dep=dept)

        if year_filter != -1:
            fees_qs = fees_qs.filter(year=year_filter)

        if academic_year != "---":
            fees_qs = fees_qs.filter(academic_year__academic_year=academic_year)

        if reg_no:
            fees_qs = fees_qs.filter(student__roll_no2__iexact=reg_no)  # Case-insensitive match

        if bal:
            fees_qs = fees_qs.filter(balance__gt=0)

        if is_lateral:
            fees_qs = fees_qs.filter(student__Is_lateral=True)
        if is_snq:
            fees_qs=fees_qs.filter(student__category='SNQ')

        # Process the filtered queryset
        for i in fees_qs:
            total += i.total_fees
            collection += i.collection
            balance += i.balance
            count += 1

            # Fetch payment history for the student
            history = [
                Collection(j.fees_receipt_no, j.date, j.total_fees)
                for j in History.objects.filter(student=i.student, year=i.year)
            ]
            student_list.append(Fees_Collection(i, history))

        # Sort the student list alphabetically if required
        if display_alphabetically:
            student_list.sort(key=lambda x: x.student.student.name)
        else:
            student_list = student_list[::-1]

        year_list = Academic_Year.objects.all()
        dep_list = department_choices

        context = {
            'student_list': student_list,
            'year_list': year_list[::-1],
            'dep_list': dep_list,
            'total': total,
            'collection': collection,
            'balance': balance,
            'dept': dept,
            'only_balance': bal,
            'academic_year': academic_year,
            'reg_no': reg_no,
            'year': year,
            'is_lateral': is_lateral,
            'is_snq':is_snq,
            'display_alphabetically': display_alphabetically,
        }
        return render(request, 'fees_updation_summary.html', context)

    # Default GET request handling
    student_list = []
    for i in Fees_Details.objects.filter(student__cancel_admission=False):
        total += i.total_fees
        collection += i.collection
        balance += i.balance
        count += 1

        history = [
            Collection(j.fees_receipt_no, j.date, j.total_fees)
            for j in History.objects.filter(student=i.student, year=i.year)
        ]
        student_list.append(Fees_Collection(i, history))

    year_list = Academic_Year.objects.all()
    dep_list = department_choices

    context = {
        'student_list': student_list[::-1],
        'year_list': year_list[::-1],
        'dep_list': dep_list,
        'total': total,
        'collection': collection,
        'balance': balance,
        'dept': "",
        'only_balance': "",
        'academic_year': "",
        'reg_no': "",
        'year': "",
        'is_lateral': False,
        'display_alphabetically': False,
    }
    return render(request, 'fees_updation_summary.html', context)
    
    pass

@login_required
def update_form(request,roll_no,year,academic_year):
    if not request.user.is_superuser:
        return HttpResponse("<h1>Permission denied!!</h1>")
    student=Student.objects.get(roll_no2=roll_no)
    fees=Fees_Details.objects.get(student=student,year=year,academic_year=academic_year)
    if request.method=='POST':
        roll_no=request.POST.get('roll_no')
        year=request.POST.get('year')
        amount=request.POST.get('amount')
        receipt_no=request.POST.get('receipt_no')
        receipt_no=int(receipt_no)
        date=Date.objects.get(pk="1").date
        try:
            hist = History.objects.get(pk=receipt_no)
            print(hist,"Hello")
            return render(request,'fee_reciept_exist.html')
        except:
            year=int(year)
            amount=int(amount)
            context={}
            if year==1 or (year==2 and student.year_completed==0) or student.category=='SNQ':
                
                if fees.collection<1370:
                    if amount>=1370:
                        tution_fees=amount-1370
                        hist=History(pk=receipt_no,student=student,year=fees.year,academic_year=fees.academic_year.academic_year,tution_fees=tution_fees,
                                admission_fees=30,id_fees=10,management_fees=60,lib_fees=150,assn_fees=60,
                                rr_fees=100,swf_fees=25,twf_fees=25,
                                lab_fees=300,sp_fees=70,nss_fees=40,dev_fees=500,date=date)
                        hist.total_fees=hist.tution_fees+ hist.admission_fees + hist.id_fees + hist.management_fees + hist.lib_fees + hist.assn_fees + hist.rr_fees + hist.swf_fees + hist.twf_fees + hist.lab_fees+ hist.sp_fees+ hist.nss_fees+ hist.dev_fees
                        hist.save()
                        fees.collection+=hist.total_fees
                        fees.balance=fees.total_fees-fees.collection
                        fees.save()
                        if fees.balance==0:
                            fees.student.year_completed+=1
                            fees.student.save()
                        context['hist']=hist
                        return render(request,'print_reciept.html',context)
                    else:
                        hist=History(fees_receipt_no=receipt_no,student=student,year=fees.year,academic_year=fees.academic_year.academic_year,tution_fees=amount,date=date)
                        hist.total_fees=hist.tution_fees+ hist.admission_fees + hist.id_fees + hist.management_fees + hist.lib_fees + hist.assn_fees + hist.rr_fees + hist.swf_fees + hist.twf_fees + hist.lab_fees+ hist.sp_fees+ hist.nss_fees+ hist.dev_fees
                        hist.save()
                        fees.collection+=hist.total_fees
                        fees.balance=fees.total_fees-fees.collection
                        fees.save()
                        if fees.balance==0:
                            fees.student.year_completed+=1
                            fees.student.save()
                        context['hist']=hist
                        return render(request,'print_reciept.html',context)
                else:
                    hist=History(fees_receipt_no=receipt_no,student=student,year=fees.year,academic_year=fees.academic_year.academic_year,tution_fees=amount,date=date)
                    hist.total_fees=hist.tution_fees+ hist.admission_fees + hist.id_fees + hist.management_fees + hist.lib_fees + hist.assn_fees + hist.rr_fees + hist.swf_fees + hist.twf_fees + hist.lab_fees+ hist.sp_fees+ hist.nss_fees+ hist.dev_fees
                    hist.save()
                    fees.collection+=hist.total_fees
                    fees.balance=fees.total_fees-fees.collection
                    fees.save()
                    if fees.balance==0:
                        fees.student.year_completed+=1
                        fees.student.save()
                    context['hist']=hist
             
                    return render(request,'print_reciept.html',context)
            else:
                if fees.collection<1220:
                    if amount>=1220:
                        tution_fees=amount-1220
                        hist=History(pk=receipt_no,student=student,year=fees.year,academic_year=fees.academic_year.academic_year,tution_fees=tution_fees,
                                admission_fees=30,id_fees=10,management_fees=60,lib_fees=0,assn_fees=60,
                                rr_fees=100,swf_fees=25,twf_fees=25,
                                lab_fees=300,sp_fees=70,nss_fees=40,dev_fees=500,date=date)
                        hist.total_fees=hist.tution_fees+ hist.admission_fees + hist.id_fees + hist.management_fees + hist.lib_fees + hist.assn_fees + hist.rr_fees + hist.swf_fees + hist.twf_fees + hist.lab_fees+ hist.sp_fees+ hist.nss_fees+ hist.dev_fees
                        hist.save()
                        fees.collection+=hist.total_fees
                        fees.balance=fees.total_fees-fees.collection
                        fees.save()
                        if fees.balance==0:
                            fees.student.year_completed+=1
                            fees.student.save()
                        context['hist']=hist
                        return render(request,'print_reciept.html',context)
                    else:
                        hist=History(fees_receipt_no=receipt_no,student=student,year=fees.year,academic_year=fees.academic_year.academic_year,tution_fees=amount,date=date)
                        hist.total_fees=hist.tution_fees+ hist.admission_fees + hist.id_fees + hist.management_fees + hist.lib_fees + hist.assn_fees + hist.rr_fees + hist.swf_fees + hist.twf_fees + hist.lab_fees+ hist.sp_fees+ hist.nss_fees+ hist.dev_fees
                        hist.save()
                        fees.collection+=hist.total_fees
                        fees.balance=fees.total_fees-fees.collection
                        fees.save()
                        if fees.balance==0:
                            fees.student.year_completed+=1
                            fees.student.save()
                        context['hist']=hist
                        return render(request,'print_reciept.html',context)
                else:
                    hist=History(fees_receipt_no=receipt_no,student=student,year=fees.year,academic_year=fees.academic_year.academic_year,tution_fees=amount,date=date)
                    hist.total_fees=hist.tution_fees+ hist.admission_fees + hist.id_fees + hist.management_fees + hist.lib_fees + hist.assn_fees + hist.rr_fees + hist.swf_fees + hist.twf_fees + hist.lab_fees+ hist.sp_fees+ hist.nss_fees+ hist.dev_fees
                    hist.save()
                    fees.collection+=hist.total_fees
                    fees.balance=fees.total_fees-fees.collection
                    fees.save()
                    if fees.balance==0:
                        fees.student.year_completed+=1
                        fees.student.save()
                    context['hist']=hist
             
                    return render(request,'print_reciept.html',context)
                
    else:            
        context={
            'roll_no':roll_no,
            'year':year,
            'fees':fees,
            'student':student,
            'date':Date.objects.get(pk="1")
        }
        return render(request,'update_form.html',context)
       
    
       
    

def success(request):
    return render(request, 'success.html')
@login_required
def day_history(request):
    academic_year='---'
    if request.method=='POST':
        academic_year=request.POST.get('academic_year')
    st=Student.objects.get(roll_no2=".")
    day_list=[]
    for i in History.objects.all():
        if i.academic_year==academic_year or academic_year=='---':
            day_list.append(i)
    day_list=sorted(day_list,key=lambda x:x.date)
    day_list2=[]
    if len(day_list)>0: 
        min_fees_no=day_list[0].fees_receipt_no
        max_fees_no=day_list[0].fees_receipt_no    
        tution_fees= day_list[0].tution_fees
        admission_fees=day_list[0].admission_fees
        id_fees=day_list[0].id_fees
        management_fees=day_list[0].management_fees
        lib_fees=day_list[0].lib_fees
        assn_fees=day_list[0].assn_fees
        rr_fees=day_list[0].rr_fees
        swf_fees=day_list[0].swf_fees
        twf_fees=day_list[0].twf_fees
        lab_fees=day_list[0].lab_fees
        sp_fees=day_list[0].sp_fees
        nss_fees=day_list[0].nss_fees
        dev_fees=day_list[0].dev_fees
        total_fees=day_list[0].total_fees
        date=day_list[0].date
        n=len(day_list)
        
        for i in range(1,n):
            if day_list[i].date==date:
                max_fees_no=day_list[i].fees_receipt_no 
                tution_fees+= day_list[i].tution_fees
                admission_fees+=day_list[i].admission_fees
                id_fees+=day_list[i].id_fees
                management_fees+=day_list[i].management_fees
                lib_fees+=day_list[i].lib_fees
                assn_fees+=day_list[i].assn_fees
                rr_fees+=day_list[i].rr_fees
                swf_fees+=day_list[i].swf_fees
                twf_fees+=day_list[i].twf_fees
                lab_fees+=day_list[i].lab_fees
                sp_fees+=day_list[i].sp_fees
                nss_fees+=day_list[i].nss_fees
                dev_fees+=day_list[i].dev_fees
                total_fees+=day_list[i].total_fees
            else:
                temp=History(fees_receipt_no=min_fees_no+'-'+max_fees_no,student=st,tution_fees=tution_fees,
                                admission_fees=admission_fees,id_fees=id_fees,management_fees=management_fees,lib_fees=lib_fees,assn_fees=assn_fees,
                                rr_fees=rr_fees,swf_fees=swf_fees,twf_fees=twf_fees,
                                lab_fees=lab_fees,sp_fees=sp_fees,nss_fees=nss_fees,dev_fees=dev_fees
                                ,date=date,total_fees=total_fees)
                day_list2.append(temp)
                min_fees_no=day_list[i].fees_receipt_no
                max_fees_no=day_list[i].fees_receipt_no
                tution_fees= day_list[i].tution_fees
                admission_fees=day_list[i].admission_fees
                id_fees=day_list[i].id_fees
                management_fees=day_list[i].management_fees
                lib_fees=day_list[i].lib_fees
                assn_fees=day_list[i].assn_fees
                rr_fees=day_list[i].rr_fees
                swf_fees=day_list[i].swf_fees
                twf_fees=day_list[i].twf_fees
                lab_fees=day_list[i].lab_fees
                sp_fees=day_list[i].sp_fees
                nss_fees=day_list[i].nss_fees
                dev_fees=day_list[i].dev_fees
                total_fees=day_list[i].total_fees
                date=day_list[i].date    
        temp=History(fees_receipt_no=min_fees_no+'-'+max_fees_no,student=st,tution_fees=tution_fees,
                            admission_fees=admission_fees,id_fees=id_fees,management_fees=management_fees,lib_fees=lib_fees,assn_fees=assn_fees,
                            rr_fees=rr_fees,swf_fees=swf_fees,twf_fees=twf_fees,
                            lab_fees=lab_fees,sp_fees=sp_fees,nss_fees=nss_fees,dev_fees=dev_fees
                            ,date=date,total_fees=total_fees)
        day_list2.append(temp)
        print()
            
    
    context={
        'day_list':day_list2,
        'year_list':Academic_Year.objects.all(),
        'academic_year': academic_year
    }
    return render(request,'day_history.html',context)


@login_required
def student_history(request,roll_no,year):
    y=int(year)
    student_list=[]
    for i in History.objects.all():
        if i.student.roll_no2==roll_no and i.year==y:
            student_list.append(i)
    context={
        'student_list':student_list
        
    }
    return render(request,'student_history.html',context)
def print_receipt(request,receipt_no):
    hist=History.objects.get(pk=receipt_no)
    context={}
    context['hist']=hist
    return render(request,'print_reciept.html',context)   
def success(request):
    return render(request, 'success.html')


def abstract(request):
    m={} 
    total,collection,balance=0,0,0
    if request.method=="POST":
        academic_year=request.POST.get('academic_year')
        for i in Fees_Details.objects.all():
            if (i.academic_year.academic_year==academic_year or academic_year=="---") and (i.student.cancel_admission==False) and i.year!=0:
                if (i.student.dep,i.year) in m:
                    m[(i.student.dep,i.year)][0]+=i.total_fees 
                    m[(i.student.dep,i.year)][1]+=i.collection 
                    m[(i.student.dep,i.year)][2]+=i.balance 
                    m[(i.student.dep,i.year)][3]+=1
                else:
                    m[(i.student.dep,i.year)]=[i.total_fees,i.collection,i.balance,1] 
        l=[]
        for i in m:
            l.append([i[0],i[1],m[i][0],m[i][1],m[i][2],m[i][3]])
        l.sort()
        abst_list=[]
        c=1 
        total_students=0
        for i in l:
            obj=Abst(c,i[0],i[1],i[2],i[3],i[4],i[5])
            total+=i[2]
            collection+=i[3]
            balance+=i[4]
            total_students+=i[5]
            c+=1
            abst_list.append(obj) 
        abst_list.append(Abst("Total","","",total,collection,balance,total_students))
        year_list=Academic_Year.objects.all()
        context={'abst_list':abst_list,'year_list':year_list[::-1],'total':total,'collection':collection,'balance':balance,'academic_year':academic_year}
        return render(request,'abstract.html',context)
    else:
        m={}
        l=[]
        for i in Fees_Details.objects.all():
            if (i.student.cancel_admission==False) and i.year!=0:              
                if (i.student.dep,i.year) in m:
                        m[(i.student.dep,i.year)][0]+=i.total_fees 
                        m[(i.student.dep,i.year)][1]+=i.collection 
                        m[(i.student.dep,i.year)][2]+=i.balance
                        m[(i.student.dep,i.year)][3]+=1
                else:
                    m[(i.student.dep,i.year)]=[i.total_fees,i.collection,i.balance,1]
        for i in m:
            l.append([i[0],i[1],m[i][0],m[i][1],m[i][2],m[i][3]])
        l.sort()
        abst_list=[]
        c=1
        total_students=0
        for i in l: 
            obj=Abst(c,i[0],i[1],i[2],i[3],i[4],i[5])
            total+=i[2]
            collection+=i[3]
            balance+=i[4]
            total_students+=i[5]
            c+=1
            abst_list.append(obj) 
        abst_list.append(Abst("Total","","",total,collection,balance,total_students))
        year_list=Academic_Year.objects.all()
        context={'abst_list':abst_list,'year_list':year_list[::-1],'total':total,'collection':collection,'balance':balance}
        return render(request,'abstract.html',context)




def abstract2(request):
    m = {}
    total, collection, balance = 0, 0, 0

    # Initialize year-wise totals and counts
    year_totals = {1: [0, 0, 0], 2: [0, 0, 0], 3: [0, 0, 0]}  # [total_fees, collection, balance]
    lateral_totals = [0, 0, 0]  # [total_fees, collection, balance]

    # Count students for each category
   
    academic_year = None  # Initialize the academic_year variable
    academic_year = request.POST.get('academic_year')
    first_year_count=0 
    second_year_count=0 
    third_year_count=0 
    lateral_count=0
    if request.method == "POST":
        
        for entry in Fees_Details.objects.filter(student__Is_lateral=False):
            if (entry.academic_year.academic_year == academic_year or academic_year == "---") and not entry.student.cancel_admission and entry.year!=0:
                if entry.year==1:
                    first_year_count+=1
                elif entry.year==2:
                    second_year_count+=1
                else:
                    third_year_count+=1

                key = (entry.student.dep, entry.year)

                # Update the main dictionary `m`
                if key in m:
                    m[key][0] += entry.total_fees
                    m[key][1] += entry.collection
                    m[key][2] += entry.balance
                    m[key][3] += 1
                else:
                    m[key] = [entry.total_fees, entry.collection, entry.balance, 1]

                year_totals[entry.year][0] += entry.total_fees
                year_totals[entry.year][1] += entry.collection
                year_totals[entry.year][2] += entry.balance
        for entry in Fees_Details.objects.filter(student__Is_lateral=True):  # Correct field name
            if (entry.academic_year.academic_year == academic_year or academic_year == "---") and not entry.student.cancel_admission and entry.year!=0:
                if entry.year==2:
                    
                    lateral_totals[0] += entry.total_fees
                    lateral_totals[1] += entry.collection
                    lateral_totals[2] += entry.balance
                    lateral_count+=1
                else:
                    key = (entry.student.dep, entry.year)
                    print(entry.student.name,entry.student.roll_no2,entry.student.dep, entry.year,entry.student.roll_no)
                    if key in m:
                        m[key][0] += entry.total_fees
                        m[key][1] += entry.collection
                        m[key][2] += entry.balance
                        m[key][3] += 1
                    else:
                        m[key] = [entry.total_fees, entry.collection, entry.balance, 1]
                    third_year_count+=1
                    if entry.year in year_totals:
                        year_totals[entry.year][0] += entry.total_fees
                        year_totals[entry.year][1] += entry.collection
                        year_totals[entry.year][2] += entry.balance
                            
    else:
        first_year_count = Fees_Details.objects.filter(year=1, student__cancel_admission=False).count()
        lateral_count = Fees_Details.objects.filter(student__Is_lateral=True, student__cancel_admission=False).count()
        second_year_count = Fees_Details.objects.filter(year=2, student__Is_lateral=False, student__cancel_admission=False).count()
        third_year_count = Fees_Details.objects.filter(year=3, student__cancel_admission=False, student__Is_lateral=False).count()

        # Get lateral fees data
        

    # Prepare data for rendering
    abst_list = [
        Abst(c, k[0], k[1], *v) for c, (k, v) in enumerate(sorted(m.items()), 1)
    ]

    # Calculate Grand Totals
    grand_total_fees = year_totals[1][0] + lateral_totals[0] + year_totals[2][0] + year_totals[3][0]
    grand_collection = year_totals[1][1] + lateral_totals[1] + year_totals[2][1] + year_totals[3][1]
    grand_balance = year_totals[1][2] + lateral_totals[2] + year_totals[2][2] + year_totals[3][2]

    # If no POST request has been made, set academic_year to "---"
    if academic_year is None:
        academic_year = "---"

    context = {
        'abst_list': abst_list,
        'year_list': Academic_Year.objects.all()[::-1],
        'first_year_total': year_totals[1][0],
        'first_year_collection': year_totals[1][1],
        'first_year_balance': year_totals[1][2],
        'first_year_count': first_year_count,  # Added count for 1st year
        'lateral_total': lateral_totals[0],
        'lateral_collection': lateral_totals[1],
        'lateral_balance': lateral_totals[2],
        'lateral_count': lateral_count,  # Added count for lateral
        'second_year_total': year_totals[2][0],
        'second_year_collection': year_totals[2][1],
        'second_year_balance': year_totals[2][2],
        'second_year_count': second_year_count,  # Added count for 2nd year
        'third_year_total': year_totals[3][0],
        'third_year_collection': year_totals[3][1],
        'third_year_balance': year_totals[3][2],
        'third_year_count': third_year_count,  # Added count for 3rd year
        'grand_total_fees': grand_total_fees,
        'grand_collection': grand_collection,
        'grand_balance': grand_balance,
        'academic_year': academic_year,
    }

    return render(request, 'abstract2.html', context)


    

@login_required
def history(request):
    academic_year='---'
    if request.method=='POST':
        academic_year=request.POST.get('academic_year')
    st=Student.objects.get(roll_no2=".")
    day_list=[]
    for i in History.objects.all():
        if i.academic_year==academic_year or academic_year=='---':
            day_list.append(i)
    day_list=sorted(day_list,key=lambda x:(x.date,x.fees_receipt_no))
    day_list2=[]
    if len(day_list)>0:
        day_list2.append(day_list[0])
        
    
        tution_fees= day_list[0].tution_fees
        admission_fees=day_list[0].admission_fees
        id_fees=day_list[0].id_fees
        management_fees=day_list[0].management_fees
        lib_fees=day_list[0].lib_fees
        assn_fees=day_list[0].assn_fees
        rr_fees=day_list[0].rr_fees
        swf_fees=day_list[0].swf_fees
        twf_fees=day_list[0].twf_fees
        lab_fees=day_list[0].lab_fees
        sp_fees=day_list[0].sp_fees
        nss_fees=day_list[0].nss_fees
        dev_fees=day_list[0].dev_fees
        total_fees=day_list[0].total_fees
        date=day_list[0].date
        n=len(day_list)
        
        for i in range(1,n):
            if day_list[i].date==date:
                tution_fees+= day_list[i].tution_fees
                admission_fees+=day_list[i].admission_fees
                id_fees+=day_list[i].id_fees
                management_fees+=day_list[i].management_fees
                lib_fees+=day_list[i].lib_fees
                assn_fees+=day_list[i].assn_fees
                rr_fees+=day_list[i].rr_fees
                swf_fees+=day_list[i].swf_fees
                twf_fees+=day_list[i].twf_fees
                lab_fees+=day_list[i].lab_fees
                sp_fees+=day_list[i].sp_fees
                nss_fees+=day_list[i].nss_fees
                dev_fees+=day_list[i].dev_fees
                total_fees+=day_list[i].total_fees
            else:
                temp=History(fees_receipt_no='Total',student=st,tution_fees=tution_fees,
                                admission_fees=admission_fees,id_fees=id_fees,management_fees=management_fees,lib_fees=lib_fees,assn_fees=assn_fees,
                                rr_fees=rr_fees,swf_fees=swf_fees,twf_fees=twf_fees,
                                lab_fees=lab_fees,sp_fees=sp_fees,nss_fees=nss_fees,dev_fees=dev_fees
                                ,date= '  ',total_fees=total_fees)
                day_list2.append(temp)
                temp2=History(fees_receipt_no=' ',student=st,year=' ',tution_fees='  ',
                                admission_fees= '  ',id_fees= '  ',management_fees=' ',lib_fees=' ',assn_fees=' ',
                                rr_fees=' ',swf_fees=' ',twf_fees=' ',
                                lab_fees=' ',sp_fees=' ',nss_fees=' ',dev_fees=' '
                                ,date= '  ',total_fees=" ")
                day_list2.append(temp2)
                tution_fees= day_list[i].tution_fees
                admission_fees=day_list[i].admission_fees
                id_fees=day_list[i].id_fees
                management_fees=day_list[i].management_fees
                lib_fees=day_list[i].lib_fees
                assn_fees=day_list[i].assn_fees
                rr_fees=day_list[i].rr_fees
                swf_fees=day_list[i].swf_fees
                twf_fees=day_list[i].twf_fees
                lab_fees=day_list[i].lab_fees
                sp_fees=day_list[i].sp_fees
                nss_fees=day_list[i].nss_fees
                dev_fees=day_list[i].dev_fees
                total_fees=day_list[i].total_fees
                date=day_list[i].date    
            day_list2.append(day_list[i])
        temp=History(fees_receipt_no='Total',student=st,tution_fees=tution_fees,
                            admission_fees=admission_fees,id_fees=id_fees,management_fees=management_fees,lib_fees=lib_fees,assn_fees=assn_fees,
                            rr_fees=rr_fees,swf_fees=swf_fees,twf_fees=twf_fees,
                            lab_fees=lab_fees,sp_fees=sp_fees,nss_fees=nss_fees,dev_fees=dev_fees
                            ,date= '  ',total_fees=total_fees)
        day_list2.append(temp)
        print()
            
    
    context={
        'day_list':day_list2,
        'year_list':Academic_Year.objects.all(),
        'academic_year': academic_year
    }
    return render(request,'history.html',context)


@login_required
def from_date_to_date_history(request):
    from_date = None
    to_date = None
    day_list = []
    st=Student.objects.get(roll_no2=".")
    if request.method == 'POST':
        from_date_str = request.POST.get('from_date')
        to_date_str = request.POST.get('to_date')
        
        if from_date_str and to_date_str:
            from_date = datetime.strptime(from_date_str, "%Y-%m-%d").date()
            to_date = datetime.strptime(to_date_str, "%Y-%m-%d").date()
            
            day_list = History.objects.filter(date__range=[from_date, to_date]).order_by('date', 'fees_receipt_no')
    else:
        day_list=History.objects.all()
    day_list2=[]
    if len(day_list)>0:
        day_list2.append(day_list[0])
        
    
        tution_fees= day_list[0].tution_fees
        admission_fees=day_list[0].admission_fees
        id_fees=day_list[0].id_fees
        management_fees=day_list[0].management_fees
        lib_fees=day_list[0].lib_fees
        assn_fees=day_list[0].assn_fees
        rr_fees=day_list[0].rr_fees
        swf_fees=day_list[0].swf_fees
        twf_fees=day_list[0].twf_fees
        lab_fees=day_list[0].lab_fees
        sp_fees=day_list[0].sp_fees
        nss_fees=day_list[0].nss_fees
        dev_fees=day_list[0].dev_fees
        total_fees=day_list[0].total_fees
        date=day_list[0].date
        n=len(day_list)
        
        for i in range(1,n):
            if day_list[i].date==date:
                tution_fees+= day_list[i].tution_fees
                admission_fees+=day_list[i].admission_fees
                id_fees+=day_list[i].id_fees
                management_fees+=day_list[i].management_fees
                lib_fees+=day_list[i].lib_fees
                assn_fees+=day_list[i].assn_fees
                rr_fees+=day_list[i].rr_fees
                swf_fees+=day_list[i].swf_fees
                twf_fees+=day_list[i].twf_fees
                lab_fees+=day_list[i].lab_fees
                sp_fees+=day_list[i].sp_fees
                nss_fees+=day_list[i].nss_fees
                dev_fees+=day_list[i].dev_fees
                total_fees+=day_list[i].total_fees
            else:
                temp=History(fees_receipt_no='Total',student=st,tution_fees=tution_fees,
                                admission_fees=admission_fees,id_fees=id_fees,management_fees=management_fees,lib_fees=lib_fees,assn_fees=assn_fees,
                                rr_fees=rr_fees,swf_fees=swf_fees,twf_fees=twf_fees,
                                lab_fees=lab_fees,sp_fees=sp_fees,nss_fees=nss_fees,dev_fees=dev_fees
                                ,date= '  ',total_fees=total_fees)
                day_list2.append(temp)
                temp2=History(fees_receipt_no=' ',student=st,year=' ',tution_fees='  ',
                                admission_fees= '  ',id_fees= '  ',management_fees=' ',lib_fees=' ',assn_fees=' ',
                                rr_fees=' ',swf_fees=' ',twf_fees=' ',
                                lab_fees=' ',sp_fees=' ',nss_fees=' ',dev_fees=' '
                                ,date= '  ',total_fees=" ")
                day_list2.append(temp2)
                tution_fees= day_list[i].tution_fees
                admission_fees=day_list[i].admission_fees
                id_fees=day_list[i].id_fees
                management_fees=day_list[i].management_fees
                lib_fees=day_list[i].lib_fees
                assn_fees=day_list[i].assn_fees
                rr_fees=day_list[i].rr_fees
                swf_fees=day_list[i].swf_fees
                twf_fees=day_list[i].twf_fees
                lab_fees=day_list[i].lab_fees
                sp_fees=day_list[i].sp_fees
                nss_fees=day_list[i].nss_fees
                dev_fees=day_list[i].dev_fees
                total_fees=day_list[i].total_fees
                date=day_list[i].date    
            day_list2.append(day_list[i])
        temp=History(fees_receipt_no='Total',student=st,tution_fees=tution_fees,
                            admission_fees=admission_fees,id_fees=id_fees,management_fees=management_fees,lib_fees=lib_fees,assn_fees=assn_fees,
                            rr_fees=rr_fees,swf_fees=swf_fees,twf_fees=twf_fees,
                            lab_fees=lab_fees,sp_fees=sp_fees,nss_fees=nss_fees,dev_fees=dev_fees
                            ,date= '  ',total_fees=total_fees)
        day_list2.append(temp)
        print()
            
    
    context = {
        'day_list': day_list,
        'from_date': from_date_str if from_date else '',
        'to_date': to_date_str if to_date else ''
    }
    
    return render(request, 'from_date_to_date_history.html', context)

@login_required 
def update_usn(request):
    if request.method=='POST':
        temp_usn=request.POST.get('usn')
        perm_usn=request.POST.get('usn2')
        obj=Student.objects.get(roll_no=temp_usn)
        obj.roll_no2=perm_usn 
        obj.save() 
        return HttpResponseRedirect(reverse('success')) 
    else:
        student_list=Student.objects.all()
        context={'student_list':student_list}
        return render(request,'update_usn.html',context)
    pass

def appln_fee(request):
    if request.method=='POST':
        amount=int(request.POST.get('amount'))
        name=request.POST.get('name')
        academic_year=request.POST.get('academic_year')
        receipt_no=request.POST.get('receipt_no')
        try:
            hist = Application_Fees.objects.get(pk=receipt_no)
            return render(request,'fee_reciept_exist.html')
        except:
            appln_obj=Application_Fees()
            appln_obj.name=name 
            appln_obj.amount=amount 
            appln_obj.academic_year=Academic_Year.objects.get(pk=academic_year)
            appln_obj.fees_receipt_no=receipt_no
            appln_obj.save()
            return HttpResponseRedirect(reverse('success'))
    else:
        context={
            'year_list':Academic_Year.objects.all()[::-1]
        }
        return render(request,'appln_fee.html',context)
    
def appln_fee_total(request):
    if request.method=='POST':
        academic_year=request.POST.get('academic_year')
        appln_list=[]
        total=0
        for i in Application_Fees.objects.all():
            if i.academic_year.academic_year==academic_year:
                total+=i.amount 
                appln_list.append(i)
        appln_list.append(Application_Fees(name="Total",amount=total))
        context={
            'year_list':Academic_Year.objects.all()[::-1],
            'appln_list':appln_list
        }
        return render(request,'appln_fee_total.html',context)
    else:
        context={
            'year_list':Academic_Year.objects.all()[::-1],
            'appln_list':[]
        }
        return render(request,'appln_fee_total.html',context)
    
def update_date(request):
    date=Date.objects.get(pk="1")
    if request.method=='POST':
        date.date=request.POST.get('date')
        date.save()
    context={
        'date':Date.objects.get(pk="1")
    }
    return render(request,'update_date.html',context)


def admission_order(request):
    if request.method=='POST':
        year=request.POST.get('year')
        year=int(year)
        student_list = Student.objects.exclude(name='.').filter(admission_year=year)
        context={
            'student_list':student_list,
            'total': len(student_list)
        }
        return render(request, 'admission_order.html', context)
    else:
        context={
            
        }
        return render(request, 'admission_order.html', context)


def print_order(request,roll_no):
    hist=Student.objects.get(pk=roll_no)
    curr_academic_year = list(Fees_Details.objects.filter(student = hist))
    print(curr_academic_year)
    curr_academic_year = curr_academic_year[0].academic_year
    context={}
    
    for i in hist.history_set.all():
        temp=i
        break
    context={
        'hist':hist,
        'fees_receipt':temp,
        'curr_academic_year':curr_academic_year
    }
    return render(request,'print_order.html',context)


def pending_fees(request):
    total, collection, balance = 0, 0, 0
    count = 0
    academic_year = " "
    year_s = " "
    dep_s = " "
    alphabetical = request.POST.get('alphabetical') == 'on'  # Check if checkbox is selected

    if request.method == "POST":
        dept = request.POST.get('dept')
        year = request.POST.get('year')
        academic_year = request.POST.get('academic_year')
        student_list = []
        y = -1
        if year != "---":
            y = int(year)
        
        for i in Fees_Details.objects.all():
            if (i.year == y or y == -1) and (i.student.dep == dept or dept == "---") and \
               (i.academic_year.academic_year == academic_year or academic_year == "---") and \
               i.balance > 0 and not i.student.cancel_admission:
                
                total += i.total_fees
                collection += i.collection
                balance += i.balance
                count += 1
                student_list.append(i)
        
        # Sort student_list alphabetically if checkbox is selected
        if alphabetical:
            student_list.sort(key=lambda x: x.student.name.lower())  # Sort ignoring case

        year_list = Academic_Year.objects.all()
        context = {
            'student_list': student_list,  # No need to reverse if alphabetical sort applied
            'year_list': year_list[::-1],
            'total': total,
            'collection': collection,
            'balance': balance,
            'dept': dept,
            'academic_year': academic_year,
            'year': year,
            'alphabetical': alphabetical  # Pass checkbox state to the template
        }
        return render(request, 'pending_fees.html', context)
    else:
        year_list = Academic_Year.objects.all()
        context = {
            'student_list': [],
            'year_list': year_list[::-1],
            'total': total,
            'collection': collection,
            'balance': balance,
            'dept': "",
            'academic_year': "",
            'year': "",
            'alphabetical': False  # Checkbox not selected by default
        }
        return render(request, 'pending_fees.html', context)

    

@login_required
def cancelled_admissions(request):

    total,collection,balance=0,0,0
    count=0
    academic_year=" "
    year_s=" "
    dep_s=" "
    if request.method=="POST":
        academic_year=request.POST.get('academic_year')
        student_list=[]
        for i in Fees_Details.objects.all():
            if (i.academic_year.academic_year==academic_year or academic_year=="---") and (i.student.cancel_admission==True) and i.year==1:
                
                total+=i.total_fees
                collection+=i.collection
                balance+=i.balance
                count+=1
                history=[]
                for j in History.objects.filter(student=i.student).filter(year=i.year):
                   history.append(Collection(j.fees_receipt_no,j.date,j.total_fees))
                student_list.append(Fees_Collection(i,history))

                
        year_list=Academic_Year.objects.all()
        context={'student_list':student_list[::-1],'total':total,'collection':collection,'balance':balance,'academic_year':academic_year, 'year_list': Academic_Year.objects.all()}
        return render(request,'cancelled_admissions.html',context)
    else:
        context={
            'student_list':[],
            'total':"",'collection':"",'balance':"",'academic_year':"",
            'year_list': Academic_Year.objects.all()
        }
        return render(request,'cancelled_admissions.html',context)
        pass

@login_required
def student_details(request):
    academic_year_id = request.GET.get('academic_year')
    students = Student.objects.all()
    academic_year = None

    if academic_year_id:
        try:
            academic_year = Academic_Year.objects.get(pk=academic_year_id)
            students = students.filter(
                fees_details__academic_year=academic_year
            ).distinct()
        except Academic_Year.DoesNotExist:
            students = Student.objects.none()  # No students if academic year does not exist

    # Fetch all academic years for the filter dropdown
    academic_years = Academic_Year.objects.all()

    # Prepare student details including the year of the fee details
    student_details = []
    for student in students:
        try:
            fee_detail = Fees_Details.objects.get(student=student, academic_year=academic_year)
        except Fees_Details.DoesNotExist:
            fee_detail = None

        student_details.append({
            'student': student,
            'year': fee_detail.year if fee_detail else None,
        })

    context = {
        'academic_years': academic_years,
        'students': student_details,
        'academic_year': academic_year_id,  # Add the current academic year ID to the context
    }
    return render(request, 'student_details.html', context)





    
    
def sub_category(request):
    m={} 
    student_count=0
    if request.method=="POST":
        academic_year=request.POST.get('academic_year')
        for i in Fees_Details.objects.all():
            if (i.academic_year.academic_year==academic_year):
                if i.student.sub_category in m:
                    m[i.student.sub_category]+=1
                else:
                    m[i.student.sub_category]=1
                student_count+=1
        l=[]
        for i in m:
            obj=Sub_Category(i,m[i])
            l.append(obj)
        l.append(Sub_Category("Total",student_count))
        year_list=Academic_Year.objects.all()
        context={'abst_list':l,'year_list':year_list[::-1],'academic_year':academic_year}
        return render(request,'sub_category.html',context)
    else:
        year_list=Academic_Year.objects.all()
        context={'abst_list':[],'year_list':year_list[::-1]}
        return render(request,'sub_category.html',context)
    
class SC_ST_STATS:
    def __init__(self,name,year,usn,cat,gender):
        self.name=name 
        self.year=year 
        self.usn=usn
        self.cat=cat
        if gender=='M':
            self.gender="Boys"
        elif gender=='F':
            self.gender='Girls'
        else:
            self.gender=gender

def sc_st_stats(request):
    year_list=Academic_Year.objects.all()
    
    if request.method=='POST':
        sc_st_list=[]
        academic_year=request.POST.get('academic_year')
        m={}
        for i in Fees_Details.objects.filter(student__cancel_admission=False):
            if (i.academic_year.academic_year==academic_year and (i.student.category=="SC" or i.student.category=="ST")):
                if (i.student.category,i.student.gender,i.year) in m:
                    m[(i.student.category,i.student.gender,i.year)]+=1 
                else:
                    m[(i.student.category,i.student.gender,i.year)]=1 
                sc_st_list.append(SC_ST_STATS(i.student.name,i.year,i.student.roll_no2,i.student.category,i.student.gender))
        for i in m:
            sc_st_list.append(SC_ST_STATS("",i[2],"",i[0],i[1]))

        sc_st_list.sort(key=lambda x:(x.cat,x.gender,x.year,x.name))
        sc_st_list2=[]
        for i in sc_st_list:
            if i.name=="" and i.usn=="":
                i.name=i.cat 
                i.usn=i.gender 
                temp=""
                if i.gender=='Boys':
                    temp="M"
                else:
                    temp='F'
                i.year=m[(i.cat,temp,i.year)]
                sc_st_list2.append(i)
                sc_st_list2.append(SC_ST_STATS("Name","Year","Reg No","",""))
            else:
                sc_st_list2.append(i)

        context={'sc_st_list':sc_st_list2,'year_list':year_list[::-1],'academic_year':academic_year}
        return render(request,'sc_st_stats.html',context)
    else:
        sc_st_list=[]
        context={'sc_st_list':sc_st_list,'year_list':year_list[::-1]}
        return render(request,'sc_st_stats.html',context)
    pass

