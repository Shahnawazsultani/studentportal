from django.shortcuts import render , HttpResponse, redirect
from django.contrib import messages
from .models import *
from .invoiceViews import *
from Profile.financeViews import *
# Create your views here.

def HOME_PAGE(request):
  # render default home page
  return render(request, "Profile/home.html")


def ALL_COURSES(request):
  if request.user.is_authenticated:
    # get all courses
    try:
        allCourses = Course.objects.all().order_by('?')
        allEnrollments = Enrollment.objects.filter(user=request.user)
        if not allEnrollments:
            allEnrollments = None

        context={
            'courses' :allCourses,
            'Enrollments': allEnrollments,
            'title': "All Courses"
        }
        return render(request, "Course/courseList.html",context)
        
    except:
        messages.error(request, "Something went wrong")
        return redirect('home')
  else:
      messages.error(request, "Please Login to perform this Action")
      return redirect("home")


def FIND_A_COURSE(request):
    if request.user.is_authenticated:
        # try to find courses with query
        try:
            query = request.GET.get('query')
            if query:
                courses = Course.objects.filter(title__icontains=query)
                if not courses:
                    courses = None
                context={
                    'courses':courses,
                    'title':"Search Result",
                    'query':query
                }
                return render(request, 'Course/courseList.html', context)
            else:
                messages.error(request, "Enter a valid query")        
            return redirect('home')
        except:
            messages.error(request, "Something went wrong")
    else:
        messages.error(request, "Please login to continue")
        return redirect('home')


def ENROLLED_COURSES(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to continue")
        return redirect('home')
    try:
        # get all courses enrolled by user
        enrollments = Enrollment.objects.filter(user=request.user)
        enrolled_courses = [enrollment.course for enrollment in enrollments]
        courses = Course.objects.filter(id__in=[course.id for course in enrolled_courses])
        context = {'courses': courses,'title':"My Enrollments"}
        return render(request, 'Course/courseList.html', context)
        
    except:
        messages.error(request, "Something went wrong")
        return redirect("home")


def CHECK_COURSE(request, id):
    try:
        # get course by course id
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return redirect("home")
    try:
        enrolled = Enrollment.objects.get(course=course, user=request.user)
    except Enrollment.DoesNotExist:
        enrolled = None
    context = {'course': course, 'enrolled': enrolled}
    return render(request, 'Course/courseView.html', context)


def COURSE_CHECKOUT(request, id):
    try:
        if request.user.is_authenticated:
            if not request.user.is_student:
                # create student finance account if not created
                createdAccount = REGISTER_FINANCE_ACCOUNT(request.user)
                if createdAccount:
                    messages.success(request, "Student Account Created Successfully!")
            course = Course.objects.get(id=id)
            if request.user in course.enrolledBy.all():
                # check if user has already enrolled in the course
                messages.info(request, "You have already enrolled in this course")
                return redirect('courseView', id=course.id)
            try:
                # create invoice for the course fee
                response = REGISTER_NEW_INVOICE(float(course.amount), GET_NEXT_THREE_DAYS_DATE(3), "TUITION_FEES", request.user.student_id)
              
            except Exception as e:
                messages.error(request, f"Failed to enroll in the course. Please try again later. Error: {e}")
                return redirect('courseView', id=course.id)
            
            if response["is_created"]:
                # add user to enrolledBy list and create enrollment
                course.enrolledBy.add(request.user)
                Enrollment.objects.create(reference=response['reference'], course=course, user=request.user)
                messages.success(request, "Course Enrolled Successfully!")
                messages.success(request, f"Your invoice refrence is : {response['reference']}")
                return redirect('courseView', id=course.id)
            else:
                messages.error(request, "Failed to create invoice. Please try again later.")
                return redirect('courseView', id=course.id)
           
        else:
            messages.error(request, "Please login to perform this action.")
            return redirect('home')
    except Course.DoesNotExist:
        messages.error(request, "Course does not exist.")
        return redirect('home')
    except Exception as e:
        print(f"An error occurred: {e}")
        messages.error(request, "An error occurred. Please try again later.")
        return redirect('home')


def ENROLL_CANCEL(request, id):
    try:
        # find enrollment by course id and user id
        course = Course.objects.get(id=id)
        enrollment = Enrollment.objects.get(course=course, user=request.user)
        try:
          # make a request to cancel invoice
          cancelStatus = DELETE_INVOICE_BY_REFERENCE(enrollment.reference)
          if cancelStatus['status'] == 200 or cancelStatus['status']==404:
            enrollment.delete()
            # remove user from enrolledBy list
            course.enrolledBy.remove(request.user)
          messages.info(request, cancelStatus['message'])
        except Exception as e:
          print(e)
          messages.error(request, "Something Went Wrong Please try again later")
        return redirect('courseView', id=course.id)
    except Course.DoesNotExist:
        messages.error(request,"Course not found")
        return redirect('home')
    
    except Enrollment.DoesNotExist:
        messages.warning(request, "Enrollment not found")
        return redirect('courseView', id=course.id)
    
    except Exception as e:
        messages.error(request, e)
        return redirect('home')


def PAY_COURSE_FEE(request,id):
    try:
        course = Course.objects.get(id=id)
        enrollment = Enrollment.objects.get(course=course, user=request.user)
        pay = PAY_INVOICE_BY_REFERENCE(enrollment.reference)
        messages.info(request, pay['message'])
        return redirect('courseView', id=course.id)
    except Exception as e:
        print(e)

