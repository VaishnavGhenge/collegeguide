from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from . models import (Cities, CollegeCourses, Contact, Courses, Email, Images, )
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import CollegeUser
from django.contrib.auth.models import User, Group
import re
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from datetime import datetime

################################## Website Home Views ########################################
# Home page
def home(request):
    return render(request, 'index.html')

# About page
def about(request):
    return render(request, 'about.html')

# Contact page
def contact(request):
    return render(request, 'contact.html')

# Contact form submission (form action view)
def submit_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        try:
            Contact(name=name, email=email, subject=subject, message=message).save()
            message = { 'msg': 'OK' }
            return JsonResponse(message)
        except ValidationError:
            data = { 'statusText': 'Form validation error', 'status': 'Error'}
            return JsonResponse(data)

# Email form submission (form action view)
def submit_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            Email(email=email).save()
            data = { 'is_submit': True }
        except ValidationError:
            data = { 'is_submit': False }
        
        return JsonResponse(data)

############################ End of Website Home Views ###########################

############################# Signin and Logout Views ######################################
# Sign in page
def signin(request):
    return render(request, 'signin.html')

# Sign in form submission (form action view)
def submit_signin(request):
    next = request.POST.get('next')
    print(next, '\n')
    if request.method == 'POST':
        email = request.POST.get('inputEmail')
        password = request.POST.get('inputPassword')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.last_login is None or user.last_login == '':
                CollegeUser.objects.filter(email=email).update(is_first=True)

            group = None
            if user.groups.exists():
                group = user.groups.all()[0].name

            login(request, user)
            msg = { 'success': True, 'group': group }
        else:
            msg = { 'success': False }
        return JsonResponse(msg)


def user_logout(request):
    user = request.user
    group = None
    if user.groups.exists():
        group = user.groups.all()[0].name
    if group == 'college':
        CollegeUser.objects.filter(email=user).update(is_first=False)
    logout(request)
    return redirect('signin')

############################# End of Signin and Logout Views ######################################

############################# Institute Views ######################################
@login_required(login_url='signin')
def institute_home(request):
    user = CollegeUser.objects.get(email=request.user)
    is_first = user.is_first
    data = {
        'colleges': CollegeUser.objects.all(),
        'nirf_colleges': CollegeUser.objects.exclude(nirfRanking=0).order_by('nirfRanking'),
        'courses': Courses.objects.all(),
        'is_first': is_first,
    }
    return render(request, 'institute-home.html', data)

@login_required(login_url='signin')
def institute_search(request):
    return render(request, 'institute-search.html')

@login_required(login_url='signin')
def institute_account(request):
    user_obj = CollegeUser.objects.get(email=request.user)
    data = {
        'college_courses': CollegeCourses.objects.filter(userId=user_obj),
        'user': user_obj,
        'posts': Images.objects.filter(userId=request.user),
        'courses': Courses.objects.all(),
    }
    return render(request, 'institute-account.html', data)

def institute_signup(request):
    data = {
        'cities': Cities.objects.all(),
    }
    return render(request, 'institute-signup.html', data)

def submit_institute_signup(request):
    if request.method == 'POST' and request.FILES['idproof']:
        profile = request.FILES.get('profile')
        backprof = request.FILES.get('backprof')
        name = request.POST.get('collegeName')
        website = request.POST.get('profileWebsite')
        description = request.POST.get('profileDescription')
        location = request.POST.get('location')
        pin = request.POST.get('pin')
        collegeType = request.POST.get('collegeType')
        foundation = request.POST.get('foundation')
        idproof = request.FILES.get('idproof')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            try:
                user = User.objects.create_user(email, email, password1)
                group = Group.objects.get(name='college')
                user.groups.add(group)
                if profile is None:
                    profile = 'user/avatar.png'
                if backprof is None:
                    backprof = 'user/default-back.jpeg'
                collegeuser = CollegeUser(collegeId=user, username=username, name=name, profileImage=profile, backgroundImage=backprof, profileDescription=description, profileWebsite=website, location=location, postalcode=pin, college_type=collegeType, college_foundation_date=foundation, email=email)
                collegeuser.save()
                print("Success\n\n")
                msg = { 'success': True }
                return JsonResponse(msg)
            except (ValidationError):
                print("Error ala\n\n")
                msg = { 'success': False}
                return JsonResponse(msg)

@login_required(login_url='signin')
def courses_submit(request):
    courses = list()
    courses = request.POST.getlist('select-courses')
    try:
        for course in courses:
            if Courses.objects.filter(courseName=course).exists():
                course_obj = Courses.objects.get(courseName=course)
                user_obj = CollegeUser.objects.get(email=request.user)
                CollegeCourses(courseId=course_obj, userId=user_obj).save()
        msg = { 'success': True }
    except ValidationError:
        msg = { 'success': False }
    return JsonResponse(msg)

@login_required(login_url='signin')
def submit_institute_post(request):
    if request.method == 'POST' and request.FILES['post-image']:
        description = request.POST.get('post-text')
        image = request.FILES.get('post-image')
        date = datetime.now().date()
        print(date, description, image)
        try:
            user_obj = User.objects.get(username=request.user)
            post = Images(userId=user_obj, image=image, title=description, date=date)
            post.save()
            msg = {'success': True,}
        except ValidationError:
            msg = {'success': False,}
        return JsonResponse(msg)


def check(request):
    username = request.GET.get('username', None)
    if len(str(username)) < 4:
        data = {
            'counterror': True,
        }
    else:
        data = {
        'is_taken': CollegeUser.objects.filter(username__iexact=username).exists(),
        'counerror': False,
    }
    return JsonResponse(data)

def check_email(request):
    email = request.GET.get('email', None)
    pattern = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(pattern, email):
        data = {
            'counterror': True,
        }
    else:
        data = {
        'is_taken': User.objects.filter(email__iexact=email).exists(),
        'counerror': False,
    }
    return JsonResponse(data)

############################# End of Institute Views ######################################

def errorcode404(request):
    return render(request, '404.html')