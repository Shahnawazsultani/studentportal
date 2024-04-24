from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from uuid import uuid4
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .financeViews import * 
from .libraryViews import *
# Create your views here.


@csrf_exempt
def registerUser(request):
    #check the request method
    if request.method == 'POST':
        try:
            # getting all values from form.
            username = request.POST['username']
            email = request.POST['email']
            pass1 = request.POST['password']
            pass2 = request.POST['confirmPassword']
            # check for error inputs
            if len(username) > 10:
                messages.error(request, 'Username must be less then 10 characters')
                return redirect('home') 
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
                return redirect('home')
            if not username.isalnum():
                messages.error(request, 'Username should only contain letters and number.')
                return redirect('home') 
            if pass1 != pass2:
                messages.error(request, 'Passwords do not match please check it again.')
                return redirect('home')
            # if no error then create a new user
            newUser = User.objects.create_user(username, email, pass1)

            if newUser is not None:
                messages.success(request, 'Student Account Created Successfully!')
                # if new uer is created then create his/her library account
                libraryAccountCreated = REGISTER_LIBRARY_ACCOUNT(newUser.student_id)
                if libraryAccountCreated:
                    messages.success(request, "Library Account Created - Default PIN is 000000")
                else:
                    messages.warning(request, "Failed to Create library Account! Ensure Module is Running")
            else:
                messages.warning(request, "Something went wrong while registering user")
                return redirect('home')
            return redirect('home')
        except Exception as e:
            
            messages.error(request, "Something Went Wrong")
            return redirect('home')
            
    else:
        return HttpResponse('bad request')


@csrf_exempt
def loginUser(request):
     #check the request method
     if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #check if user has entered correct credentials
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Logged in')
            return redirect('home')
        else:
            messages.error(request,"Login Failed, Please try again with correct username and password.")
            return redirect('home')
     else:
        return HttpResponse('404 page not found.')


def logoutUser(request):
    # logout current user
    logout(request)
    messages.success(request,'Successfully Logged Out')
    return redirect('home')


def UPDATE_USER_PROFILE(request):
    # check the request method 
    if request.method == 'POST':
        # get the new data from the form
        new_email = request.POST.get('email')
        new_username = request.POST.get('username')
        new_first_name = request.POST.get('fName')
        new_last_name = request.POST.get('lName')
        
        # Check if the new email already exists
        if new_email != request.user.email and User.objects.filter(email=new_email).exists():
            messages.warning(request, "Email already registered. Please use another")
            return redirect("userProfile")

        # Check if the new username already exists
        if new_username != request.user.username and User.objects.filter(username=new_username).exists():
            messages.warning(request, "username already registered. Please use another")
            return redirect("userProfile")
        #update student info 
        user = request.user
        user.email = new_email
        user.username = new_username
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.save()
        
        messages.success(request, "Profile Updated Successfully")
        
        return redirect('userProfile') 
    

def USER_DASHBOARD(request):
    student_invoices = None
    if request.user.is_authenticated:
        try:
            # get student invoices from finance module
            student_invoices = STUDENT_INVOICES(request.user.student_id)
            if not student_invoices:
                student_invoices = None
            elif student_invoices == True:
                messages.error(request, "Please Start Finance & Library Apps first")
                return redirect('home')
            context = {'user': request.user, 'invoices': student_invoices}
            return render(request, 'profile/profile.html', context)
        except Exception as e:
            messages.error(request, 'An error occurred while processing your request.')
            return redirect('home')
    else:
        messages.error(request, 'Please Login to continue')
        return redirect('home')


def GRADUATION_STATUS(request):
    if request.user.is_authenticated:
        try:
            # check if student has an account in finance module - if yes then get all invoices of requested user
            check_status = STUDENT_INFO(request.user.student_id)
            if check_status['error'] == True:
                messages.error(request, "Start Finance & Library Module First")
                return redirect("home")
            elif check_status['hasAccount'] == True and check_status['hasOutStandingBalance']==True:
                context = {'hasOutStandingBalance':True}
                return render(request, "Profile/graduation.html", context)
            
            elif check_status['hasAccount'] == True and check_status['hasOutStandingBalance']==False:
                context = {'noOutStandingBalance':True}
                return render(request, "Profile/graduation.html", context)
            
            elif check_status['hasAccount'] == False:
                context = {'invalidStudent': True, 'hasOutStandingBalance': False}
                return render(request, "Profile/graduation.html", context)

            else:
                messages.error(request, "Student Account Not Found")
                return redirect("home")
        except Exception as e:
            return redirect('home')
    else:
        messages.error(request, "Please Login to perform this Action")
        return redirect('home')
    

def TRY_TO_CREATE_LIBRARY_ACCOUNT(request):
    if request.user.is_authenticated:
        # try to create library account
        created = REGISTER_LIBRARY_ACCOUNT(request.user.student_id)
        if created:
            messages.success(request, "Library Account Created Successfully! Default PIN: 000000")
            return redirect("userProfile")
        else:
            messages.error(request, "Something Went Wrong")
            return redirect("userProfile")
    else:
        messages.error(request, "Please Login to perform this action.")
        return redirect("home")