import json
from django.core.mail.message import EmailMultiAlternatives
from django.db.models.expressions import Col
from django.http.response import HttpResponse
from collegeapp.decorators import admin_only, allowed_users, unauthenticated_user
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from . models import (Cities, CollegeCourses, CollegeReview, Collegehelpful, Contact, CourseReview, Coursehelpful, Courses, Email, Followers,
                      ImageLikes, Images, Like, PLatformStatistics, StudentUser, )
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import CollegeUser
from django.contrib.auth.models import User, Group
import re
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from itertools import chain
import random
from django.core.mail import BadHeaderError
import math
import os
import requests

################################## Website Home Views ########################################
# Home page
def index(request):
    stat = PLatformStatistics.objects.get(id=1)
    count = stat.platformVisitors
    count += 1
    PLatformStatistics.objects.filter(id=1).update(platformVisitors=count)

    students = StudentUser.objects.all().count()
    colleges = CollegeUser.objects.all().count()
    courses = Courses.objects.all().count()
    PLatformStatistics.objects.filter(id=1).update(
        platformVisitors=count, studentUsers=students, collegeUsers=colleges, totalCourses=courses)

    stat = PLatformStatistics.objects.get(id=1)
    nirf_colleges = CollegeUser.objects.exclude(
        nirfRanking=0).order_by('nirfRanking')[:8]
    all_courses = Courses.objects.all()

    data = {
        'nirf_colleges': nirf_colleges,
        'stat': stat, 
        'courses': all_courses, 
    }
    return render(request, 'index.html', data)

# About page
def about(request):
    stat = PLatformStatistics.objects.get(id=1)
    count = stat.platformVisitors
    count += 1
    PLatformStatistics.objects.filter(id=1).update(platformVisitors=count)

    data = {'stat': stat,  }
    return render(request, 'about.html', data)


# Contact page
def contact(request):
    stat = PLatformStatistics.objects.get(id=1)
    count = stat.platformVisitors
    count += 1
    PLatformStatistics.objects.filter(id=1).update(platformVisitors=count)

    return render(request, 'contact.html')

# Contact form submission (form action view)
def submit_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        date = datetime.now()
        try:
            Contact(name=name, email=email, subject=subject,
                    message=message, date=date).save()
            message = {'msg': 'OK'}
            return JsonResponse(message)
        except ValidationError:
            data = {'statusText': 'Form validation error', 'status': 'Error'}
            return JsonResponse(data)

# Email form submission (form action view)
def submit_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            Email(email=email).save()
            data = {'is_submit': True}
        except ValidationError:
            data = {'is_submit': False}

        return JsonResponse(data)

############################ End of Website Home Views ###########################

############################# Signin and Logout Views ######################################
# Sign in page
@unauthenticated_user
def signin(request):
    stat = PLatformStatistics.objects.get(id=1)
    count = stat.platformVisitors
    count += 1
    PLatformStatistics.objects.filter(id=1).update(platformVisitors=count)

    return render(request, 'signin.html')


# Sign in form submission (form action view)
@unauthenticated_user
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
            msg = {'success': True, 'group': group}
        else:
            msg = {'success': False}
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

############################# Acount Views ######################################


@login_required(login_url='signin')
@allowed_users(allowed_roles=['college', 'student'])
def home(request):
    stat = PLatformStatistics.objects.get(id=1)
    count = stat.platformVisitors
    count += 1
    PLatformStatistics.objects.filter(id=1).update(platformVisitors=count)

    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name

    # Check if users first time login or not to show course form
    user = None
    suggested_collges = None
    if group == 'college':
        user = CollegeUser.objects.get(email=request.user)
        suggested_collges = CollegeUser.objects.filter(city=user.city).exclude(collegeId=user.collegeId).order_by('totalSum')[:8]
    elif group == 'student':
        user = StudentUser.objects.get(email=request.user)
        query1 = CollegeUser.objects.filter(city=user.prefLocation).order_by('-totalSum')[:8]
        # print("all colleges: ", query1)
        suggested_collges = list()
        for college in query1:
            college_courses = CollegeCourses.objects.filter(userId=college)
            # print("all courses: ", college_courses)
            for course in college_courses:
                cos = Courses.objects.get(courseId=course.courseId_id)
                if str(cos.courseName) == user.prefCourse1:
                    if college not in suggested_collges:
                        suggested_collges.append(college)
                if str(cos.courseName) == user.prefCourse2:
                    if college not in suggested_collges:
                        suggested_collges.append(college)
                if str(cos.courseName) == user.prefCourse3:
                    if college not in suggested_collges:
                        suggested_collges.append(college)
        # print("suggested: ", suggested_collges)
    elif group == 'admin':
        return redirect('dashboard')
    is_first = user.is_first

    # Get all liked colleges by requesr.user
    liked_col = Like.objects.filter(user1=request.user).order_by('-likeId')
    liked_colleges = list()
    for col in liked_col:
        liked_colleges = liked_colleges + \
            list(chain(CollegeUser.objects.filter(collegeId=col.user2)))

    # Followed colleges
    followed_col = Followers.objects.filter(
        user1=request.user).order_by('-followId')
    followed_colleges = list()
    for col in followed_col:
        followed_colleges = followed_colleges + \
            list(chain(CollegeUser.objects.filter(collegeId=col.user2)))

    # Getting highest ranked colleges by nirf
    nirf_colleges = CollegeUser.objects.exclude(
        nirfRanking=0).order_by('nirfRanking')[:8]

    data = {
        'liked_colleges': liked_colleges,
        'followed_colleges': followed_colleges,
        'nirf_colleges': nirf_colleges,
        'courses': Courses.objects.all(),
        'is_first': is_first,
        'group': group,
        'suggested_collges': suggested_collges,
    }
    return render(request, 'home.html', data)

###################################


@login_required(login_url='signin')
def search(request):
    stat = PLatformStatistics.objects.get(id=1)
    count = stat.platformVisitors
    count += 1
    PLatformStatistics.objects.filter(id=1).update(platformVisitors=count)

    search_response = None
    followed_colleges = None
    liked_colleges = None

    if 'btn-search' in request.GET:
        city = request.GET.get('select-city')
        stream = request.GET.get('select-stream')
        college = request.GET.get('select-college')

        print(city, stream, college, '\n\n')

        if city == '' and stream == '' and college != '':
            search_response = CollegeUser.objects.filter(email=college)
        elif city != '' and stream == '' and college != '':
            search_response = CollegeUser.objects.filter(
                email=college, city=city)
        elif city != '' and stream == '' and college == '':
            search_response = CollegeUser.objects.filter(city=city).order_by('-totalSum')
        elif city != '' and stream != '' and college == '':
            response1 = CollegeCourses.objects.filter(courseId=stream)
            response2 = list()
            for col in response1:
                response2 = response2 + \
                    list(chain(CollegeUser.objects.filter(collegeId=col.userId),))
            search_response = list()
            for col in response2:
                search_response = search_response + \
                    list(chain(CollegeUser.objects.filter(
                        collegeId=col.collegeId, city=city),))
        elif city == '' and stream != '' and college == '':
            response1 = CollegeCourses.objects.filter(courseId=stream)
            search_response = list()
            for col in response1:
                search_response = search_response + \
                    list(chain(CollegeUser.objects.filter(collegeId=col.userId),))

        # Followed colleges
        followed_col = Followers.objects.filter(user1=request.user)
        followed_colleges = list()
        for col in followed_col:
            followed_colleges = followed_colleges + \
                list(chain(CollegeUser.objects.filter(collegeId=col.user2)))

        # Get all liked colleges by requesr.user
        liked_col = Like.objects.filter(user1=request.user)
        liked_colleges = list()
        for col in liked_col:
            liked_colleges = liked_colleges + \
                list(chain(CollegeUser.objects.filter(collegeId=col.user2)))

    data = {
        'cities': Cities.objects.all(),
        'streams': Courses.objects.all(),
        'colleges': CollegeUser.objects.all(),
        'search_response': search_response,
        'liked_colleges': liked_colleges,
        'followed_colleges': followed_colleges,
    }
    return render(request, 'search.html', data)

####################################


@login_required(login_url='signin')
@allowed_users(allowed_roles=['college', 'student'])
def account(request, id=0):
    stat = PLatformStatistics.objects.get(id=1)
    count = stat.platformVisitors
    count += 1
    PLatformStatistics.objects.filter(id=1).update(platformVisitors=count)

    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name

    if group == 'college':
        user_obj = CollegeUser.objects.get(email=request.user)
        posts = Images.objects.filter(userId=request.user).order_by('-imageId')
        postCount = Images.objects.filter(userId=request.user).count()
        liked = ImageLikes.objects.filter(userId=request.user).values()
        ids = list()
        for like in liked:
            ids.append(like.get('imageId_id'))

        collegeReviews = CollegeReview.objects.filter(collegeId=user_obj).order_by('-date')
        collegeReviews_tmp = CollegeReview.objects.filter(collegeId=user_obj).values()
        college_reviewed_users = list()
        student_list = list()
        for review in collegeReviews_tmp:
            if review.get('studentId_id') in student_list:
                continue
            else:
                college_reviewed_users = college_reviewed_users + \
                    list(chain(StudentUser.objects.filter(
                        studentId=review.get('studentId_id'))))
                student_list.append(review.get('studentId_id'))
        col_reviewed = Collegehelpful.objects.filter(userid=request.user, college=user_obj)

        colnot = []
        for help in col_reviewed:
            colnot.append(help.reviewid)

        CourseReviews = CourseReview.objects.filter(
            collegeId=user_obj).order_by('-date')
        courseReviews_tmp = CourseReview.objects.filter(
            collegeId=user_obj).values()
        course_reviewed_users = list()
        student_list = list()
        for review in courseReviews_tmp:
            if review.get('studentId_id') in student_list:
                continue
            else:
                course_reviewed_users = course_reviewed_users + \
                    list(chain(StudentUser.objects.filter(
                        studentId=review.get('studentId_id'))))
                student_list.append(review.get('studentId_id'))
        cos_reviewed = Coursehelpful.objects.filter(userid=request.user, college=user_obj)

        cosnot = []
        for help in cos_reviewed:
            cosnot.append(help.reviewid)

        college_helpfuls = Collegehelpful.objects.filter(
            userid=request.user, college=user_obj)
        course_helpfuls = Coursehelpful.objects.filter(
            userid=request.user, college=user_obj)

        if isinstance(id, int):
            if id > 0:
                id = int(id)
                if Images.objects.filter(imageId=id, userId=request.user).exists():
                    Images.objects.filter(imageId=id).delete()
                    count = user_obj.postCount
                    count -= 1
                    user_obj.postCount = count
                    user_obj.save()
                else:
                    return redirect('account')
        else:
            return redirect('account')

        data = {
            'college_courses': CollegeCourses.objects.filter(userId=user_obj),
            'user': user_obj,
            'posts': posts,
            'courses': Courses.objects.all(),
            'selfliked': Like.objects.filter(user2=request.user).exists(),
            'ids': ids,
            'postCount': postCount,
            'group': 'college',
            'collegeReviews': collegeReviews,
            'CourseReviews': CourseReviews,
            'college_reviewed_users': college_reviewed_users,
            'course_reviewed_users': course_reviewed_users,
            'college_helpfuls': college_helpfuls,
            'course_helpfuls': course_helpfuls,
            'colhelped': colnot,
            'coshelped': cosnot,
        }
    if group == 'student':
        user_obj = StudentUser.objects.get(email=request.user)
        posts = Images.objects.filter(userId=request.user).order_by('-imageId')
        postCount = Images.objects.filter(userId=request.user).count()
        liked = ImageLikes.objects.filter(userId=request.user).values()
        ids = list()
        for like in liked:
            ids.append(like.get('imageId_id'))

        if isinstance(id, int):
            if id > 0:
                id = int(id)
                if Images.objects.filter(imageId=id, userId=request.user).exists():
                    Images.objects.filter(imageId=id).delete()
                    count = user_obj.postCount
                    count -= 1
                    user_obj.postCount = count
                    user_obj.save()
                else:
                    return redirect('account')
        else:
            return redirect('account')

        data = {
            'user': user_obj,
            'posts': posts,
            'selfliked': Like.objects.filter(user2=request.user).exists(),
            'ids': ids,
            'postCount': postCount,
            'group': 'student',
        }

    return render(request, 'account.html', data)


@login_required(login_url='signin')
def view_account(request, group, username):
    stat = PLatformStatistics.objects.get(id=1)
    count = stat.platformVisitors
    count += 1
    PLatformStatistics.objects.filter(id=1).update(platformVisitors=count)

    username = str(username)
    group = str(group)

    if group == 'college':
        user = CollegeUser.objects.get(username=username)

        if user.email == request.user.email:
            return redirect('account')

        if user is not None:
            college = User.objects.get(email=user.email)
            # Get all liked colleges by login user for checking current profile is liked by him or not
            liked_colleges = Like.objects.filter(user1=request.user)
            liked = 'false'
            for like in liked_colleges:
                if user.collegeId == like.user2:
                    liked = 'true'

            # Get all followed colleges by login user for checking current profile is followed by him or not
            followed_colleges = Followers.objects.filter(user1=request.user)
            followed = 'false'
            for follow in followed_colleges:
                if user.collegeId == follow.user2:
                    followed = 'true'

            courses = CollegeCourses.objects.filter(userId=user).values()
            college_courses = list()
            for course in courses:
                college_courses = college_courses + \
                    list(chain(Courses.objects.filter(
                        courseId=course.get('courseId_id'))))
            courses = CollegeCourses.objects.filter(userId=user)

            posts = Images.objects.filter(
                userId=college.id).order_by('-imageId')
            postCount = Images.objects.filter(userId=college.id).count()

            likedposts = ImageLikes.objects.filter(
                userId=request.user).values()
            ids = list()
            for like in likedposts:
                ids.append(like.get('imageId_id'))

            collegeReviews = CollegeReview.objects.filter(
                collegeId=college.id).order_by('-date')
            collegeReviews_tmp = CollegeReview.objects.filter(
                collegeId=college.id).values()
            college_reviewed_users = list()
            student_list = list()
            for review in collegeReviews_tmp:
                if review.get('studentId_id') in student_list:
                    continue
                else:
                    college_reviewed_users = college_reviewed_users + \
                        list(chain(StudentUser.objects.filter(
                            studentId=review.get('studentId_id'))))
                    student_list.append(review.get('studentId_id'))
            col_reviewed = Collegehelpful.objects.filter(userid=request.user, college=user)

            colnot = []
            for help in col_reviewed:
                colnot.append(help.reviewid)

            CourseReviews = CourseReview.objects.filter(
                collegeId=college.id).order_by('-date')
            courseReviews_tmp = CourseReview.objects.filter(
                collegeId=college.id).values()
            course_reviewed_users = list()
            student_list = list()
            for review in courseReviews_tmp:
                if review.get('studentId_id') in student_list:
                    continue
                else:
                    course_reviewed_users = course_reviewed_users + \
                        list(chain(StudentUser.objects.filter(
                            studentId=review.get('studentId_id'))))
                    student_list.append(review.get('studentId_id'))
            cos_reviewed = Coursehelpful.objects.filter(userid=request.user, college=user)

            cosnot = []
            for help in cos_reviewed:
                cosnot.append(help.reviewid)

            visiting_user_group = None
            if request.user.groups.exists():
                visiting_user_group = request.user.groups.all()[0].name

            college_helpfuls = Collegehelpful.objects.filter(
                userid=request.user, college=user)
            course_helpfuls = Coursehelpful.objects.filter(
                userid=request.user, college=user)

            data = {
                'liked': liked,
                'followed': followed,
                'user': user,
                'college_courses': college_courses,
                'courses': courses,
                'type': 'college',
                'posts': posts,
                'postCount': postCount,
                'ids': ids,
                'collegeReviews': collegeReviews,
                'CourseReviews': CourseReviews,
                'college_reviewed_users': college_reviewed_users,
                'course_reviewed_users': course_reviewed_users,
                'visiting_user_group': visiting_user_group,
                'college_helpfuls': college_helpfuls,
                'course_helpfuls': course_helpfuls,
                'col_not_helped': colnot,
                'cos_not_helped': cosnot,
            }
            return render(request, 'visit-account.html', data)
    elif group == 'student':
        user = StudentUser.objects.get(username=username)

        if user.email == request.user.email:
            return redirect('account')

        if user is not None:
            student = User.objects.get(email=user.email)

            # Get all liked colleges by login user for checking current profile is liked by him or not
            liked_colleges = Like.objects.filter(user1=request.user)
            liked = 'false'
            for like in liked_colleges:
                if user.studentId == like.user2:
                    liked = 'true'

            # Get all followed colleges by login user for checking current profile is followed by him or not
            followed_colleges = Followers.objects.filter(user1=request.user)
            followed = 'false'
            for follow in followed_colleges:
                if user.studentId == follow.user2:
                    followed = 'true'

            posts = Images.objects.filter(
                userId=student.id).order_by('-imageId')
            postCount = Images.objects.filter(userId=student.id).count()

            likedposts = ImageLikes.objects.filter(
                userId=request.user).values()
            ids = list()
            for like in likedposts:
                ids.append(like.get('imageId_id'))

            data = {
                'liked': liked,
                'followed': followed,
                'user': user,
                'type': 'student',
                'posts': posts,
                'postCount': postCount,
                'ids': ids,
            }
            return render(request, 'visit-account.html', data)

###################################


@login_required(login_url='signin')
def likedislike(request):
    if request.method == 'POST':
        if 'purpose' in request.POST:
            user = User.objects.get(username=request.user)
            group = None
            if user.groups.exists():
                group = user.groups.all()[0].name
            try:
                if request.POST.get('purpose') == 'self-like':
                    Like(user1=user, user2=user,
                         date=datetime.now().date()).save()
                elif request.POST.get('purpose') == 'self-dislike':
                    Like.objects.filter(user1=user, user2=user).delete()
                like_count = Like.objects.filter(user2=user).count()
                if group == 'college':
                    CollegeUser.objects.filter(email=request.user).update(
                        profileLikes=like_count)
                elif group == 'student':
                    StudentUser.objects.filter(email=request.user).update(
                        profileLikes=like_count)
                msg = {'success': True, 'count': like_count, }
                return JsonResponse(msg)
            except ValidationError:
                msg = {'success': False, }
                return JsonResponse(msg)
    if request.method == 'GET':
        userid = str(request.GET.get('userid'))
        purpose = str(request.GET.get('purpose'))
        acctype = str(request.GET.get('acctype'))
        try:
            user = User.objects.get(email=userid)
            if purpose == 'like':
                Like(user1=request.user, user2=user,
                     date=datetime.now().date()).save()
            elif purpose == 'dislike':
                Like.objects.filter(user1=request.user, user2=user).delete()
            like_count = Like.objects.filter(user2=user).count()
            if acctype == 'college':
                CollegeUser.objects.filter(email=userid).update(
                    profileLikes=like_count)
            elif acctype == 'student':
                StudentUser.objects.filter(email=userid).update(
                    profileLikes=like_count)
            msg = {'success': True, 'count': like_count, }
            return JsonResponse(msg)
        except ValidationError:
            msg = {'success': False}
            return JsonResponse(msg)

###################################


@login_required(login_url='signin')
def likedislikePosts(request):
    postId = int(request.GET.get('postId'))
    purpose = request.GET.get('purpose')
    try:
        image = Images.objects.get(imageId=postId)
        if purpose == 'post-like':
            ImageLikes(imageId=image, userId=request.user,
                       date=datetime.now().date()).save()
        elif purpose == 'post-dislike':
            ImageLikes.objects.filter(
                imageId=image, userId=request.user).delete()
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


@login_required(login_url='signin')
# Follow or to Unfollow
def follow_unfollow(request):
    userid = str(request.GET.get('userid'))
    purpose = str(request.GET.get('purpose'))
    acctype = request.GET.get('acctype')

    try:
        user = User.objects.get(email=userid)
        if purpose == 'follow':
            Followers(user1=request.user, user2=user,
                      date=datetime.now().date()).save()
        elif purpose == 'unfollow':
            Followers.objects.filter(user1=request.user, user2=user).delete()
        follow_count = Followers.objects.filter(user2=user).count()
        if acctype == 'college':
            CollegeUser.objects.filter(email=userid).update(
                profileFollowers=follow_count)
        elif acctype == 'student':
            StudentUser.objects.filter(email=userid).update(
                profileFollowers=follow_count)
        msg = {'success': True, 'count': follow_count, }
    except ValidationError:
        msg = {'success': False}

    return JsonResponse(msg)

##############################

def institute_signup(request):
    stat = PLatformStatistics.objects.get(id=1)
    count = stat.platformVisitors
    count += 1
    PLatformStatistics.objects.filter(id=1).update(platformVisitors=count)

    data = {
        'cities': Cities.objects.all(),
    }
    return render(request, 'institute-signup.html', data)

####################################


def submit_institute_signup(request):
    try:
        if str(request.session['emailverified']) == 'true':
            del request.session['emailverified']
        else:
            msg = {'success': False}
            return JsonResponse(msg)
    except KeyError:
        msg = {'success': False}
        return JsonResponse(msg)

    if request.method == 'POST':
        profile = request.FILES.get('profile')
        backprof = request.FILES.get('backprof')
        name = request.POST.get('collegeName')
        website = request.POST.get('profileWebsite')
        description = request.POST.get('profileDescription')
        city = request.POST.get('city')
        pin = request.POST.get('pin')
        collegeType = request.POST.get('collegeType')
        foundation = request.POST.get('foundation')
        username = request.POST.get('username')
        email = request.session.get('email', '')
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
                                          email=email, verified=True)
                collegeuser.save()

                try:
                    del request.session['email']
                except:
                    pass
                msg = {'success': True}
                return JsonResponse(msg)
            except (ValidationError):
                msg = {'success': False}
                return JsonResponse(msg)
###########################################

@allowed_users(allowed_roles=['college'])
def institute_edit(request):
    if request.method == 'POST':
        user = CollegeUser.objects.get(collegeId=request.user)
        profile = request.FILES.get('profile')
        back = request.FILES.get('backprof')
        name = request.POST.get('collegeName')
        website = request.POST.get('profileWebsite')
        description = request.POST.get('profileDescription')

        if profile is None or profile == '':
            profile = user.profileImage
        else:
            image_path = user.profileImage.path
            if os.path.exists(image_path):
                os.remove(image_path)
        if back is None or back == '':
            back = user.backgroundImage
        else:
            image_path = user.backgroundImage.path
            if os.path.exists(image_path):
                os.remove(image_path)
        try:
            user.profileImage = profile
            user.backgroundImage = back
            user.name = name
            user.profileWebsite = website
            user.profileDescription = description
            user.save()
            msg = {'success': True, }
            return JsonResponse(msg)
        except ValidationError:
            msg = {'success': False, }
            return JsonResponse(msg)
    data = {
        'user': CollegeUser.objects.get(collegeId=request.user)
    }
    return render(request, 'institute-edit-details.html', data)
##############################


def student_signup(request):
    stat = PLatformStatistics.objects.get(id=1)
    count = stat.platformVisitors
    count += 1
    PLatformStatistics.objects.filter(id=1).update(platformVisitors=count)

    data = {
        'cities': Cities.objects.all(),
        'courses': Courses.objects.all(),
    }
    return render(request, 'student-signup.html', data)


####################################
def submit_student_signup(request):
    try:
        if str(request.session['emailverified']) == 'true':
            del request.session['emailverified']
        else:
            msg = {'success': False}
            return JsonResponse(msg)
    except KeyError:
        msg = {'success': False}
        return JsonResponse(msg)

    if request.method == 'POST':
        profile = request.FILES.get('profile')
        backprof = request.FILES.get('backprof')
        name = request.POST.get('firstname')
        surname = request.POST.get('lastname')
        description = request.POST.get('profileDescription')
        location = request.POST.get('city')
        courses = request.POST.getlist('courses')
        username = request.POST.get('username')
        email = request.session.get('email', '')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        course_count = len(courses)
        if course_count == 1:
            course1 = courses[0]
            course2 = ''
            course3 = ''
        elif course_count == 2:
            course1 = courses[0]
            course2 = courses[1]
            course3 = ''
        elif course_count == 3:
            course1 = courses[0]
            course2 = courses[1]
            course3 = courses[2]

        if password1 == password2:
            try:
                user = User.objects.create_user(email, email, password1)
                group = Group.objects.get(name='student')
                user.groups.add(group)

                if profile is None:
                    profile = 'user/avatar.png'
                if backprof is None:
                    backprof = 'user/default-back.jpeg'

                studentuser = StudentUser(studentId=user, name=name, surname=surname, profileImage=profile,
                                          backgroundImage=backprof, profileDescription=description, prefLocation=location, prefCourse1=course1,
                                          prefCourse2=course2, prefCourse3=course3, email=email, username=username)
                studentuser.save()
                try:
                    del request.session['email']
                except:
                    pass
                msg = {'success': True}
                return JsonResponse(msg)
            except (ValidationError):
                msg = {'success': False}
                return JsonResponse(msg)



@allowed_users(allowed_roles=['student'])
def student_edit(request):
    if request.method == 'POST':
        user = StudentUser.objects.get(studentId=request.user)
        profile = request.FILES.get('profile')
        back = request.FILES.get('backprof')
        name = request.POST.get('firstname')
        surname = request.POST.get('lastname')
        description = request.POST.get('profileDescription')

        if profile is None or profile == '':
            profile = user.profileImage
        else:
            image_path = user.profileImage.path
            if os.path.exists(image_path):
                os.remove(image_path)
        if back is None or back == '':
            back = user.backgroundImage
        else:
            image_path = user.backgroundImage.path
            if os.path.exists(image_path):
                os.remove(image_path)
        try:
            user.profileImage = profile
            user.backgroundImage = back
            user.name = name
            user.surname = surname
            user.profileDescription = description
            user.save()
            msg = {'success': True, }
            return JsonResponse(msg)
        except ValidationError:
            msg = {'success': False, }
            return JsonResponse(msg)
    data = {
        'user': StudentUser.objects.get(studentId=request.user)
    }
    return render(request, 'student-edit-details.html', data)
######################################


@login_required(login_url='signin')
@allowed_users(allowed_roles=['college'])
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
            CollegeUser.objects.filter(
                email=request.user).update(is_first=False)
        msg = {'success': True}
    except ValidationError:
        msg = {'success': False}
    return JsonResponse(msg)

###################################


@login_required(login_url='signin')
@allowed_users(allowed_roles=['college', 'student'])
def submit_institute_post(request):
    if request.method == 'POST' and request.FILES['post-image']:
        description = request.POST.get('post-text')
        image = request.FILES.get('post-image')
        url = request.POST.get('post-url')
        date = datetime.now()

        try:
            user_obj = User.objects.get(username=request.user)
            post = Images(userId=user_obj, image=image,
                          title=description, url=url, date=date)
            post.save()
            msg = {'success': True, }
        except ValidationError:
            msg = {'success': False, }
        return JsonResponse(msg)


@login_required(login_url='signin')
@allowed_users(allowed_roles=['student'])
def submit_college_review(request):
    if request.method == 'POST':
        text = request.POST.get('college-review')
        campus_rating = int(request.POST.get('campus-input'))
        library_rating = int(request.POST.get('library-input'))
        userid = str(request.POST.get('userid'))
        captcha_token = request.POST.get('g-recaptcha-response', '')

        if captcha_token == '':
            msg = { 'success': False, }
            return JsonResponse(msg)

        # google recaptcha for human verification
        cap_url = 'https://www.google.com/recaptcha/api/siteverify'
        cap_secret = '6Lf8DPEaAAAAAD3BZjper2XlZtYkpAuuZdfj11q4'
        cap_data = { 'secret': cap_secret, 'response': captcha_token, }
        cap_server_response = requests.post(url=cap_url, data=cap_data)
        cap_json = json.loads(cap_server_response.text)
        if cap_json['success'] == False:
            msg = { 'success': False, }
            return JsonResponse(msg)

        college = CollegeUser.objects.get(email=userid)
        student = StudentUser.objects.get(email=request.user.email)
        try:
            total_rating = int(round((campus_rating+library_rating)/2))

            CollegeReview(studentId=student, collegeId=college, message=text,
                          campusRating=campus_rating, libraryRating=library_rating, date=datetime.now(), totalRating=total_rating).save()

            campus = college.campusRating
            campussum = college.campusSum
            library = college.libraryRating
            librarysum = college.librarySum
            reviewcount = college.collegeReviewCount

            totalsum = college.totalSum
            totalcount = college.totalCount
            total = college.totalRating
            if campus is None and library is None and total is None or campus == 0 and library == 0 and total == 0:
                campus = int(campus_rating)
                campussum = campus
                library = int(library_rating)
                librarysum = library
                reviewcount = 1

                totalsum = campus + library
                totalcount = 2
                total = int(round(totalsum / totalcount))
            elif campus is None and library is None and total is not None or campus == 0 and library == 0 and total != 0:
                campus = int(campus_rating)
                campussum = campus
                library = int(library_rating)
                librarysum = library
                reviewcount = 1

                totalsum = int(totalsum + (campus + library))
                totalcount = totalcount + 2
                total = int(round(totalsum / totalcount))
            elif campus is not None and library is not None or campus != 0 and library != 0:
                campussum = campussum + int(campus_rating)
                reviewcount = reviewcount + 1
                campus = int(round(campussum / reviewcount))
                librarysum = librarysum + int(library_rating)
                library = int(round(librarysum / reviewcount))

                totalsum = int(totalsum + (campus + library))
                totalcount = totalcount + 2
                total = int(round(totalsum / totalcount))
            else:
                raise ValidationError

            count = CollegeReview.objects.filter(collegeId_id=college).count(
            ) + CourseReview.objects.filter(collegeId_id=college).count()
            CollegeUser.objects.filter(email=userid).update(reviewCount=count, campusRating=campus, libraryRating=library,
                                                            totalRating=total, campusSum=campussum, librarySum=librarysum, collegeReviewCount=reviewcount, totalSum=totalsum, totalCount=totalcount)
            msg = {'success': True, }
        except ValidationError:
            msg = {'success': False, }
        return JsonResponse(msg)


@login_required(login_url='signin')
@allowed_users(allowed_roles=['student'])
def submit_course_review(request):
    if request.method == 'POST':
        courseid = request.POST.get('select-course')
        if courseid is None or courseid == '':
            msg = {'success': False, }
            return JsonResponse(msg)
        
        text = str(request.POST.get('course-review-text'))
        staff_rating = int(request.POST.get('staff-input'))
        curriculum_rating = int(request.POST.get('curriculum-input'))
        userid = str(request.POST.get('userid'))
        captcha_token = request.POST.get('g-recaptcha-response', '')

        if captcha_token == '':
            msg = { 'success': False, }
            return JsonResponse(msg)

        # google recaptcha for human verification
        cap_url = 'https://www.google.com/recaptcha/api/siteverify'
        cap_secret = '6Lf8DPEaAAAAAD3BZjper2XlZtYkpAuuZdfj11q4'
        cap_data = { 'secret': cap_secret, 'response': captcha_token, }
        cap_server_response = requests.post(url=cap_url, data=cap_data)
        cap_json = json.loads(cap_server_response.text)
        if cap_json['success'] == False:
            msg = { 'success': False, }
            return JsonResponse(msg)

        college = CollegeUser.objects.get(email=userid)
        student = StudentUser.objects.get(email=request.user.email)
        _course = Courses.objects.get(courseId=courseid)
        course = CollegeCourses.objects.get(courseId=_course, userId=college)
        try:
            total_rating = int(round((staff_rating+curriculum_rating)/2))

            CourseReview(courseId=course, collegeId=college, studentId=student, message=text,
                         staffRating=staff_rating, curriculumRating=curriculum_rating, date=datetime.now(), totalRating=total_rating).save()

            staff = college.staffRating
            staffsum = college.staffSum
            curriculum = college.curriculumRating
            curriculumsum = college.curriculumSum
            reviewcount = college.courseReviewCount

            total = college.totalRating
            totalsum = college.totalSum
            totalcount = college.totalCount

            if staff is None and curriculum is None and total is None or staff == 0 and curriculum == 0 and total == 0:
                staff = int(staff_rating)
                staffsum = staff
                curriculum = int(curriculum_rating)
                curriculumsum = curriculum
                reviewcount = 1

                totalsum = staff + curriculum
                totalcount = 2
                total = int(round(totalsum / totalcount))
            elif staff is None and curriculum is None and total is not None or staff == 0 and curriculum == 0 and total != 0:
                staff = int(staff_rating)
                staffsum = staff
                curriculum = int(curriculum_rating)
                curriculumsum = curriculum
                reviewcount = 1

                totalsum = int(totalsum + (staff + curriculum))
                totalcount = totalcount + 2
                total = int(round(totalsum / totalcount))
            elif staff is not None and curriculum is not None or staff != 0 and curriculum != 0:
                staffsum = staffsum + int(staff_rating)
                reviewcount = reviewcount + 1
                staff = int(round(staffsum / reviewcount))
                curriculumsum = curriculumsum + int(curriculum_rating)
                curriculum = int(round(curriculumsum / reviewcount))
                totalsum = int(totalsum + (staff + curriculum))
                totalcount = totalcount + 2
                total = int(round(totalsum / totalcount))
            else:
                raise ValidationError

            print('curriculum: ', curriculum)
            print('staf: ', staff)
            CollegeCourses.objects.filter(courseId=_course, userId=college).update(
                staffRating=staff, CurriculumRating=curriculum)
            count = CollegeReview.objects.filter(collegeId_id=college).count(
            ) + CourseReview.objects.filter(collegeId_id=college).count()
            CollegeUser.objects.filter(email=userid).update(reviewCount=count, totalRating=total, staffRating=staff,
                                                            curriculumRating=curriculum, courseReviewCount=reviewcount, staffSum=staffsum, curriculumSum=curriculumsum, totalSum=totalsum, totalCount=totalcount)

            msg = {'success': True, }
        except ValidationError:
            msg = {'success': False, }

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

##################################


def makesession(request, name, value):
    request.session[str(name)] = str(value)
    return HttpResponse("created")


def deletesession(request):
    try:
        del request.session['emailverified']
        del request.session['email']
        msg = 'success'
        return HttpResponse(msg)
    except:
        msg = 'error'
        return HttpResponse(msg)

##################################


def sendOTP(request):
    range_start = 10**(6-1)
    range_end = (10**6)-1
    otp = int(random.randint(range_start, range_end))
    mailto = str(request.GET.get('mailto', '')).strip()
    if mailto:
        try:
            subject, from_email, to = 'Confirmation email', 'clgguide@gmail.com', mailto
            text_content = "Don't share this one time passoword with anyone"
            html_content = "<p><strong style='color: #ffc107;'>Warning</strong><br>Don't share this one time password with anyone<br>Your OTP is <b>" + str(otp)+"</b></p>"
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            respose = makesession(request, 'otp', otp)
            respose = makesession(request, 'email', mailto)
            print(request.session['otp'])
            msg = {'success': True, }
            return JsonResponse(msg)
        except BadHeaderError:
            msg = {'success': False, }
            return JsonResponse(msg)

#############################


def checkotp(request):
    otp = request.GET.get('otp', '')
    if otp:
        if str(otp) == str(request.session['otp']):
            response = makesession(request, 'emailverified', 'true')
            del request.session['otp']
            msg = {'success': True, }
            return JsonResponse(msg)
        else:
            msg = {'success': False, }
            return JsonResponse(msg)
    else:
        msg = {'success': False, }
        return JsonResponse(msg)


def clearsession(request):
    try:
        res = deletesession(request)
        msg = {'success': True}
        return JsonResponse(msg)
    except:
        msg = {'success': False}
        return JsonResponse(msg)


def getratingstats(request):
    username = request.GET.get('college', '')
    if username != '':
        college = CollegeUser.objects.get(username=username)
        college_reviews = CollegeReview.objects.filter(collegeId=college)
        course_reviews = CourseReview.objects.filter(collegeId=college)

        total = college.reviewCount
        avg = college.totalRating
        onestar = 0
        twostar = 0
        threestar = 0
        fourstar = 0
        fivestar = 0
        for review in college_reviews:
            if int(review.campusRating) == 5:
                fivestar += 1
            if int(review.libraryRating) == 5:
                fivestar += 1
            if int(review.campusRating) == 4:
                fourstar += 1
            if int(review.libraryRating) == 4:
                fourstar += 1
            if int(review.campusRating) == 3:
                threestar += 1
            if int(review.libraryRating) == 3:
                threestar += 1
            if int(review.campusRating) == 2:
                twostar += 1
            if int(review.libraryRating) == 2:
                twostar += 1
            if int(review.campusRating) == 1:
                onestar += 1
            if int(review.libraryRating) == 1:
                onestar += 1

        for review in course_reviews:
            if int(review.staffRating) == 5:
                fivestar += 1
            if int(review.curriculumRating) == 5:
                fivestar += 1
            if int(review.staffRating) == 4:
                fourstar += 1
            if int(review.curriculumRating) == 4:
                fourstar += 1
            if int(review.staffRating) == 3:
                threestar += 1
            if int(review.curriculumRating) == 3:
                threestar += 1
            if int(review.staffRating) == 2:
                twostar += 1
            if int(review.curriculumRating) == 2:
                twostar += 1
            if int(review.staffRating) == 1:
                onestar += 1
            if int(review.curriculumRating) == 1:
                onestar += 1

        totalstars = onestar + twostar + threestar + fourstar + fivestar
        fiveper = round((fivestar/totalstars)*100, 1)
        fourper = round((fourstar/totalstars)*100, 1)
        threeper = round((threestar/totalstars)*100, 1)
        twoper = round((twostar/totalstars)*100, 1)
        oneper = round((onestar/totalstars)*100, 1)

        msg = {
            'success': True,
            'fiveper': fiveper,
            'fourper': fourper,
            'threeper': threeper,
            'twoper': twoper,
            'oneper': oneper,
            'total': total,
            'avg': avg,
        }
        return JsonResponse(msg)
    else:
        msg = {'success': False, }
        return JsonResponse(msg)

######################################

@login_required(login_url='signin')
def helpful_view(request):
    btn = request.GET.get('btn', '')
    reviewid = request.GET.get('reviewid', '')
    type = request.GET.get('rtype', '')
    username = request.GET.get('college', '')

    if btn != '' and reviewid != '' and type != '' and username != '':
        college = CollegeUser.objects.get(username=username)
        if type == 'college':
            review = CollegeReview.objects.get(reviewId=int(reviewid))
            if btn == 'yes':
                rated_review = Collegehelpful.objects.filter(
                    reviewid=review, userid=request.user, purpose='no')
                if not rated_review:
                    Collegehelpful(reviewid=review, userid=request.user,
                                   college=college, purpose='yes').save()
                    count = review.helpfulCount
                    if count is None or count == '':
                        count = 0
                    count += 1
                    CollegeReview.objects.filter(reviewId=int(
                        reviewid)).update(helpfulCount=count)

                    msg = {'success': True, 'count': count, }
                    return JsonResponse(msg)
                else:
                    # Collegehelpful.objects.filter(reviewid=review, userid=request.user, college=college, purpose='no').delete()
                    ncount = review.notHelpfulCount
                    if ncount is None or ncount == '':
                        ncount = 0
                    ncount -= 1
                    CollegeReview.objects.filter(reviewId=int(
                        reviewid)).update(notHelpfulCount=ncount)

                    Collegehelpful.objects.filter(
                        reviewid=review, userid=request.user, college=college, purpose='no').update(purpose='yes')
                    hcount = review.helpfulCount
                    if hcount is None or hcount == '':
                        hcount = 0
                    hcount += 1
                    CollegeReview.objects.filter(reviewId=int(
                        reviewid)).update(helpfulCount=hcount)

                    msg = {'success': True, 'ncount': ncount,
                           'hcount': hcount, 'update': True, }
                    return JsonResponse(msg)
            elif btn == 'no':
                rated_review = Collegehelpful.objects.filter(
                    reviewid=review, userid=request.user, purpose='yes')
                if not rated_review:
                    Collegehelpful(reviewid=review, userid=request.user,
                                   college=college, purpose='no').save()
                    count = review.notHelpfulCount
                    if count is None or count == '':
                        count = 0
                    count += 1
                    CollegeReview.objects.filter(reviewId=int(
                        reviewid)).update(notHelpfulCount=count)

                    msg = {'success': True, 'count': count, }
                    return JsonResponse(msg)
                else:
                    # Collegehelpful.objects.filter(reviewid=review, userid=request.user, college=college, purpose='yes').delete()
                    hcount = review.helpfulCount
                    if hcount is None or hcount == '':
                        hcount = 0
                    hcount -= 1
                    CollegeReview.objects.filter(reviewId=int(
                        reviewid)).update(helpfulCount=hcount)

                    Collegehelpful.objects.filter(
                        reviewid=review, userid=request.user, college=college, purpose='yes').update(purpose='no')
                    ncount = review.notHelpfulCount
                    if ncount is None or ncount == '':
                        ncount = 0
                    ncount += 1
                    CollegeReview.objects.filter(reviewId=int(
                        reviewid)).update(notHelpfulCount=ncount)
                    msg = {'success': True, 'ncount': ncount,
                           'hcount': hcount, 'update': True, }
                    return JsonResponse(msg)
        elif type == 'course':
            review = CourseReview.objects.get(reviewId=int(reviewid))
            if btn == 'yes':
                rated_review = Coursehelpful.objects.filter(
                    reviewid=review, userid=request.user, purpose='no')
                if not rated_review:
                    Coursehelpful(reviewid=review, userid=request.user,
                                  college=college, purpose='yes').save()
                    count = review.helpfulCount
                    if count is None or count == '':
                        count = 0
                    count += 1
                    CourseReview.objects.filter(reviewId=int(
                        reviewid)).update(helpfulCount=count)

                    msg = {'success': True, 'count': count, }
                    return JsonResponse(msg)
                else:
                    # Coursehelpful.objects.filter(reviewid=review, userid=request.user, college=college, purpose='no').delete()
                    ncount = review.notHelpfulCount
                    if ncount is None or ncount == '':
                        ncount = 0
                    ncount -= 1
                    CourseReview.objects.filter(reviewId=int(
                        reviewid)).update(notHelpfulCount=ncount)

                    Coursehelpful.objects.filter(
                        reviewid=review, userid=request.user, college=college, purpose='no').update(purpose='yes')
                    hcount = review.helpfulCount
                    if hcount is None or hcount == '':
                        hcount = 0
                    hcount += 1
                    CourseReview.objects.filter(reviewId=int(
                        reviewid)).update(helpfulCount=hcount)

                    msg = {'success': True, 'ncount': ncount,
                           'hcount': hcount, 'update': True, }
                    return JsonResponse(msg)
            elif btn == 'no':
                rated_review = Coursehelpful.objects.filter(
                    reviewid=review, userid=request.user, purpose='yes')
                if not rated_review:
                    Coursehelpful(reviewid=review, userid=request.user,
                                  college=college, purpose='no').save()
                    count = review.notHelpfulCount
                    if count is None or count == '':
                        count = 0
                    count += 1
                    CourseReview.objects.filter(reviewId=int(
                        reviewid)).update(notHelpfulCount=count)

                    msg = {'success': True, 'count': count, }
                    return JsonResponse(msg)
                else:
                    # Coursehelpful.objects.filter(reviewid=review, userid=request.user, college=college, purpose='yes').delete()
                    hcount = review.helpfulCount
                    if hcount is None or hcount == '':
                        hcount = 0
                    hcount -= 1
                    CourseReview.objects.filter(reviewId=int(
                        reviewid)).update(helpfulCount=hcount)

                    Collegehelpful.objects.filter(
                        reviewid=review, userid=request.user, college=college, purpose='yes').update(purpose='no')
                    ncount = review.notHelpfulCount
                    if ncount is None or ncount == '':
                        ncount = 0
                    ncount += 1
                    CourseReview.objects.filter(reviewId=int(
                        reviewid)).update(notHelpfulCount=ncount)
                    msg = {'success': True, 'ncount': ncount,
                           'hcount': hcount, 'update': True, }
                    return JsonResponse(msg)
    else:
        msg = {'success': False, }


def courseview_pre(request, course):
    try:
        course = int(course)
        course_obj = Courses.objects.get(courseId=course)
        college_courses = CollegeCourses.objects.filter(courseId=course_obj)
        college_list = list()
        for course in college_courses:
            college_list.append(course.userId)
    except:
        return HttpResponse('Please stop playing with urls..')
    data = {
        'colleges': college_list,
        'course': course_obj.courseName,
    }
    return render(request, 'view-course-pre.html', data)

############################# End of Institute Views ######################################


def errorcode404(request):
    stat = PLatformStatistics.objects.get(id=1)
    count = stat.platformVisitors
    count += 1
    PLatformStatistics.objects.filter(id=1).update(platformVisitors=count)

    return render(request, '404.html')

def errorcode500(request):
    stat = PLatformStatistics.objects.get(id=1)
    count = stat.platformVisitors
    count += 1
    PLatformStatistics.objects.filter(id=1).update(platformVisitors=count)

    return render(request, '500.html')


###################### Dashboard #######################
@login_required(login_url='signin')
@admin_only
def dashboard(request, id=0):
    if id != 0:
        id = int(id)
        contact = Contact.objects.filter(contactId=id)
        if contact.exists():
            contact.delete()
        return redirect('dashboard')
    else:
        stat = PLatformStatistics.objects.get(id=1)
        count = stat.platformVisitors
        count += 1
        PLatformStatistics.objects.filter(id=1).update(platformVisitors=count)

    data = {
        'messages': Contact.objects.all().order_by('-date')
    }
    return render(request, 'dashboard.html', data)

@login_required(login_url='signin')
@admin_only
def admin_forms(request, type=None, id=0):
    if request.method == 'POST':
        if 'course-add' in request.POST:
            course = request.POST.get('course')
            if course != '':
                if Courses.objects.filter(courseName=course).exists():
                    return redirect('admin-forms')   
                Courses(courseName=course, date=datetime.now().date()).save()
            return redirect('admin-forms')
        elif 'city-add' in request.POST:
            city = request.POST.get('city')
            if city != '':
                if Cities.objects.filter(cityName=city).exists():
                    return redirect('admin-forms')  
                Cities(cityName=city).save()
            return redirect('admin-forms')
    elif id != 0 and type is not None:
        id = int(id)
        if str(type) == 'course':
            course = Courses.objects.filter(courseId=id)
            if course.exists():
                course.delete()
        elif str(type) == 'city':
            city = Cities.objects.filter(citiId=id)
            if city.exists():
                city.delete()
        return redirect('admin-forms')
    data = {
        'courses': Courses.objects.all().order_by('courseName'),
        'cities': Cities.objects.all().order_by('cityName'),
        'colleges': CollegeUser.objects.all().order_by('nirfRanking'),
    }
    return render(request, 'dashboard2.html', data)

@login_required(login_url='signin')
@admin_only
def editRank(request):
    if request.method == 'POST':
        rank = int(request.POST.get('rank'))
        id = str(request.POST.get('college-id'))
        if rank < 0 or id == '':
            return redirect('admin-forms')
        else:
            user = User.objects.get(email=id)
            if rank == 0:
                CollegeUser.objects.filter(collegeId=user).update(nirfRanking=rank)
            if CollegeUser.objects.filter(collegeId=user).exists:
                prevcollege = CollegeUser.objects.filter(nirfRanking=rank)
                if prevcollege:
                    prevcollege.update(nirfRanking=0)
                    CollegeUser.objects.filter(collegeId=user).update(nirfRanking=rank)
                else:
                    CollegeUser.objects.filter(collegeId=user).update(nirfRanking=rank)
            msg = {'success': True}
            return JsonResponse(msg)
    else:
        return HttpResponse('Please stop playing with our urls gentleman')