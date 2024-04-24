from django.contrib import admin
from django.urls import path, include
from . views import *
urlpatterns = [
    path('', HOME_PAGE, name="home"),
    path('course-list', ALL_COURSES, name="courseList"),
    path('myEnrollments', ENROLLED_COURSES, name="myEnrollments"),
    path('course/<int:id>/', CHECK_COURSE, name="courseView"),
    path('enrollCourse/<int:id>/', COURSE_CHECKOUT, name="enrollCourse"),
    path('cancelEnrollment/<int:id>/', ENROLL_CANCEL, name="cancelEnrollment"),
    path('payInvoice/<int:id>/', PAY_COURSE_FEE, name="payInvoice"),
    path('searchCourse', FIND_A_COURSE, name="searchCourse")
    

]
