from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from . models import (Cities, CollegeCourses, Contact, Courses, Email, ImageLikes, Images, Like, )
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import CollegeUser
from django.contrib.auth.models import User, Group
import re
from django.contrib.auth.decorators import login_required
from datetime import datetime
from itertools import chain

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
    liked_col = Like.objects.filter(user1=request.user)
    liked_colleges = list()
    for col in liked_col:
        liked_colleges = liked_colleges + list(chain(CollegeUser.objects.filter(collegeId=col.user2)))
    data = {
        'liked_colleges': liked_colleges,
        'nirf_colleges': CollegeUser.objects.exclude(nirfRanking=0).order_by('nirfRanking'),
        'courses': Courses.objects.all(),
        'is_first': is_first,
    }
    return render(request, 'institute-home.html', data)

###################################
@login_required(login_url='signin')
def institute_search(request):
    search_response = None
    if 'btn-search' in request.GET:
        city = request.GET.get('select-city')
        stream = request.GET.get('select-stream')
        college = request.GET.get('select-college')

        print(city, stream, college, '\n\n')

        if city == '' and stream == '' and college != '':
            search_response = CollegeUser.objects.filter(email=college)
        elif city != '' and stream == '' and college != '':
            search_response = CollegeUser.objects.filter(email=college, city=city)
        elif city != '' and stream == '' and college == '':
            search_response = CollegeUser.objects.filter(city=city)
        elif city != '' and stream != '' and college == '':
            response1 = CollegeCourses.objects.filter(courseId=stream)
            response2 = list()
            for col in response1:
                response2 = response2 + list(chain(CollegeUser.objects.filter(collegeId=col.userId),))
            search_response = list()
            for col in response2:
                search_response =  search_response + list(chain(CollegeUser.objects.filter(collegeId=col.collegeId, city=city),))
        elif city == '' and stream != '' and college == '':
            response1 = CollegeCourses.objects.filter(courseId=stream)
            search_response = list()
            for col in response1:
                search_response = search_response + list(chain(CollegeUser.objects.filter(collegeId=col.userId),))
            
    data = {
        'cities': Cities.objects.all(),
        'streams': Courses.objects.all(),
        'colleges': CollegeUser.objects.all(),
        'search_response': search_response,
    }
    return render(request, 'institute-search.html', data)

####################################
@login_required(login_url='signin')
def institute_account(request):
    user_obj = CollegeUser.objects.get(email=request.user)
    posts = Images.objects.filter(userId=request.user).order_by('-date')
    liked = ImageLikes.objects.filter(userId=request.user).values()
    ids = list()
    for like in liked:
        ids.append(like.get('imageId_id'))

    data = {
        'college_courses': CollegeCourses.objects.filter(userId=user_obj),
        'user': user_obj,
        'posts': posts,
        'courses': Courses.objects.all(),
        'selfliked': Like.objects.filter(user2=request.user).exists(),
        'ids': ids,
    }
  
    return render(request, 'institute-account.html', data)

###################################
@login_required(login_url='signin')
def likedislike(request):
    if request.method == 'POST':
        if 'purpose' in request.POST:
                user = User.objects.get(username=request.user)
                try:
                    if request.POST.get('purpose') == 'self-like':
                        Like(user1=user, user2=user, date=datetime.now().date()).save()
                    elif request.POST.get('purpose') == 'self-dislike':
                        Like.objects.filter(user1=user, user2=user).delete()
                    like_count = Like.objects.filter(user2=user).count()
                    CollegeUser.objects.filter(email=request.user).update(profileLikes=like_count)
                    msg = {
                        'success': True,
                        'count': like_count,
                    }
                    return JsonResponse(msg)
                except ValidationError:
                    msg = {
                        'success': False,
                    }
                    return JsonResponse(msg)

###################################
@login_required(login_url='signin')
def likedislikePosts(request):
    postId = int(request.GET.get('postId'))
    purpose = request.GET.get('purpose')
    try:
        image = Images.objects.get(imageId=postId)
        if purpose == 'post-like':
            ImageLikes(imageId=image, userId=request.user, date=datetime.now().date()).save()
        elif purpose == 'post-dislike':
            ImageLikes.objects.filter(imageId=image, userId=request.user).delete()
        likeCount = ImageLikes.objects.filter(imageId=image).count()
        Images.objects.filter(imageId=postId).update(totalLikes=likeCount)
        msg = {
            'success': True,
            'count': likeCount,
        }
    except ValidationError:
        msg = {
            'success': False,
        }
    return JsonResponse(msg)

##############################
def institute_signup(request):
    data = {
        'cities': Cities.objects.all(),
    }
    return render(request, 'institute-signup.html', data)

####################################
def submit_institute_signup(request):
    if request.method == 'POST' and request.FILES['idproof']:
        profile = request.FILES.get('profile')
        backprof = request.FILES.get('backprof')
        name = request.POST.get('collegeName')
        website = request.POST.get('profileWebsite')
        description = request.POST.get('profileDescription')
        city = request.POST.get('city')
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

                collegeuser = CollegeUser(collegeId=user, username=username, name=name, profileImage=profile,
                backgroundImage=backprof, profileDescription=description, profileWebsite=website,
                city=city, postalcode=pin, college_type=collegeType, college_foundation_date=foundation,
                email=email)

                collegeuser.save()
                msg = { 'success': True }
                return JsonResponse(msg)
            except (ValidationError):
                print("Error ala\n\n")
                msg = { 'success': False}
                return JsonResponse(msg)

######################################
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
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'college':
            CollegeUser.objects.filter(email=request.user).update(is_first=False)
        msg = { 'success': True }
    except ValidationError:
        msg = { 'success': False }
    return JsonResponse(msg)

###################################
@login_required(login_url='signin')
def submit_institute_post(request):
    if request.method == 'POST' and request.FILES['post-image']:
        description = request.POST.get('post-text')
        image = request.FILES.get('post-image')
        date = datetime.now()
        try:
            user_obj = User.objects.get(username=request.user)
            post = Images(userId=user_obj, image=image, title=description, date=date)
            post.save()
            msg = {'success': True,}
        except ValidationError:
            msg = {'success': False,}
        return JsonResponse(msg)

###################
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

##########################
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