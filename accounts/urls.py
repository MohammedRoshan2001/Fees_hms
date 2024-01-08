from django.urls import path
from . import views
from django.contrib import admin
urlpatterns = [
    path('',views.index,name="index"),
    path('add',views.add_student,name="add"),
    path('success',views.success,name="success"),
    path('history',views.history,name="history"),
    path('day_history',views.day_history,name="day_history"),
    path('update_usn',views.update_usn,name="update_usn"),
    path('fees_updation',views.fees_updation,name="fees_updation"),
    path('abstract',views.abstract,name="abstract"),
    path('update_form/<str:roll_no>/<int:year>',views.update_form,name="update_form"),
    path('student_history/<str:roll_no>/<int:year>',views.student_history,name="student_history"),
    path('print_receipt/<str:receipt_no>',views.print_receipt,name="print_receipt"),
    path('appln_fee',views.appln_fee,name="appln_fee"),
    path('appln_fee_total',views.appln_fee_total,name="appln_fee_total"),
    path('update_date',views.update_date,name="update_date"),
    path('admission_order',views.admission_order,name="admission_order"),
    path('print_order/<str:roll_no>',views.print_order,name="print_order"),
    path('add_data',views.add_data,name="add_data"),
    path('pending_fees',views.pending_fees,name="pending_fees"),
    path('cancelled_admissions',views.cancelled_admissions,name="cancelled_admissions"),
    path('sub_category',views.sub_category,name="sub_category"),
    path('sc_st_stats',views.sc_st_stats,name="sc_st_stats"),
    

]