
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


def index(request):
    print(len(Fees_Details.objects.all()))
    s = set()
    for i in Fees_Details.objects.all():
        s.add((i.student, i.year, i.academic_year))
    print(len(s))
    return render(request, 'base.html')



def add_student(request):
    if request.method=="POST":
        usn=request.POST.get('usn')
        year=request.POST.get('year')
        st=Student.objects.get(roll_no2=usn)
        y=int(year)
        try:
            st=Fees_Details.objects.get(student=st,year=y)
            return render(request,'student_exist.html')
        except:
            total_fee=-1
            if st.category=='SNQ':
                    total_fee=1370
            elif st.year_completed==0:
                total_fee=6998
            else:
                total_fee=6848
                
                
            academic_year1=request.POST.get('academic_year')
            academic_year=Academic_Year.objects.get(academic_year=academic_year1)
        
            fees_obj=Fees_Details(student=st,year=y,academic_year=academic_year,total_fees=total_fee,balance=total_fee)
            fees_obj.save()
            return HttpResponseRedirect(reverse('success'))
    else:
        student_list=Student.objects.all()
        year_list=Academic_Year.objects.all()
        context={'student_list':student_list,'year_list':year_list[::-1]}
        return render(request,'add_student.html',context)
    pass
def fees_updation(request):
    total, collection, balance = 0, 0, 0
    count = 0
    academic_year = " "
    year_s = " "
    dep_s = " "

    if request.method == "POST":
        dept = request.POST.get('dept')
        year = request.POST.get('year')
        academic_year = request.POST.get('academic_year')
        bal = request.POST.get('bal')
        reg_no = request.POST.get('reg_no').upper()
        display_alphabetically = request.POST.get('display_alphabetically')

        student_list = []
        y = -1
        if year != "---":
            y = int(year)
        for i in Fees_Details.objects.all():
            if (i.year == y or y == -1) and (i.student.dep == dept or dept == "---") and (
                    i.academic_year.academic_year == academic_year or academic_year == "---") and (
                    reg_no == "" or i.student.roll_no2.upper() == reg_no) and (bal == None or i.balance > 0) and (
                    i.student.cancel_admission == False):

                total += i.total_fees
                collection += i.collection
                balance += i.balance
                count += 1
                history = []
                for j in History.objects.filter(student=i.student).filter(year=i.year):
                    history.append(Collection(j.fees_receipt_no, j.date, j.total_fees))
                student_list.append(Fees_Collection(i, history))

        year_list = Academic_Year.objects.all()
        if display_alphabetically == '1':
            student_list.sort(key=lambda x: x.student.student.name)
        else:
            student_list = student_list[::-1]

        context = {'student_list': student_list, 'year_list': year_list[::-1], 'total': total,
                   'collection': collection, 'balance': balance, 'dept': dept, 'only_balance': bal,
                   'academic_year': academic_year, 'reg_no': reg_no, 'year': year}
        return render(request, 'fees_updation.html', context)
    else:
        student_list = []
        for i in Fees_Details.objects.all():
            if (i.student.cancel_admission == False):
                total += i.total_fees
                collection += i.collection
                balance += i.balance
                count += 1
                history = []
                for j in History.objects.filter(student=i.student).filter(year=i.year):
                    history.append(Collection(j.fees_receipt_no, j.date, j.total_fees))
                student_list.append(Fees_Collection(i, history))
        year_list = Academic_Year.objects.all()
        context = {'student_list': student_list[::-1], 'year_list': year_list[::-1], 'total': total,
                   'collection': collection, 'balance': balance, 'dept': "", 'only_balance': "", 'academic_year': "",
                   'reg_no': "", 'year': ""}
        return render(request, 'fees_updation.html', context)


                        
                
                
        
   
    pass
@login_required
def update_form(request,roll_no,year):
    if not request.user.is_superuser:
        return HttpResponse("<h1>Permission denied!!</h1>")
    student=Student.objects.get(roll_no2=roll_no)
    fees=Fees_Details.objects.get(student=student,year=year)
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
            'student':student
        }
        return render(request,'update_form.html',context)
       
    

def success(request):
    return render(request, 'success.html')
@login_required
def day_history(request):
    st=Student.objects.get(roll_no2=".")
    day_list=History.objects.all()
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
        'day_list':day_list2
    }
    for i in day_list2:
        print(i)
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
            if (i.academic_year.academic_year==academic_year or academic_year=="---"):
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
        context={'abst_list':abst_list,'year_list':year_list[::-1],'total':total,'collection':collection,'balance':balance}
        return render(request,'abstract.html',context)
    else:
        m={}
        l=[]
        for i in Fees_Details.objects.all():              
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


@login_required
def history(request):
    st=Student.objects.get(roll_no2=".")
    day_list=History.objects.all()
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
        'day_list':day_list2
    }
    for i in day_list2:
        print(i)
    return render(request,'history.html',context)

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
    context={}
    
    for i in hist.history_set.all():
        temp=i
        break
    print(hist,temp)
    context={
        'hist':hist,
        'fees_receipt':temp
    }
    return render(request,'print_order.html',context)


def pending_fees(request):
    total,collection,balance=0,0,0
    count=0
    academic_year=" "
    year_s=" "
    dep_s=" "
    if request.method=="POST":
        dept=request.POST.get('dept')
        year=request.POST.get('year')
        academic_year=request.POST.get('academic_year')
        student_list=[]
        y=-1 
        if year!="---":
            y=int(year)
        for i in Fees_Details.objects.all():
            if (i.year==y or y==-1) and (i.student.dep==dept or dept=="---") and (i.academic_year.academic_year==academic_year or academic_year=="---") and  i.balance>0 and i.student.cancel_admission==False:
                
                total+=i.total_fees
                collection+=i.collection
                balance+=i.balance
                count+=1
                student_list.append(i)

                
        year_list=Academic_Year.objects.all()
        context={'student_list':student_list[::-1],'year_list':year_list[::-1],'total':total,'collection':collection,'balance':balance,'dept':dept,'academic_year':academic_year,'year':year}
        return render(request,'pending_fees.html',context)
    else:
        year_list=Academic_Year.objects.all()
        context={'student_list':[],'year_list':year_list[::-1],'total':total,'collection':collection,'balance':balance,'dept':"",'academic_year':"",'year':""}
        return render(request,'pending_fees.html',context)
    

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
        for i in Fees_Details.objects.all():
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

