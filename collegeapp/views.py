from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from . models import (Cities, CollegeCourses, CollegeReview, Contact, CourseReview, Courses, Email, Followers, ImageLikes, Images, Like, StudentUser, )
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import CollegeUser
from django.contrib.auth.models import User, Group
import re
from django.contrib.auth.decorators import login_required
from datetime import datetime
from itertools import chain, permutations

################################## Website Home Views ########################################
# Home page
def index(request):
    nirf_colleges = CollegeUser.objects.exclude(nirfRanking=0).order_by('nirfRanking')
    data = { 'nirf_colleges': nirf_colleges, }
    return render(request, 'index.html', data)

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
def home(request):
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name

    # Check if users first time login or not to show course form
    user = None
    if group == 'college':
        user = CollegeUser.objects.get(email=request.user)
    elif group == 'student':
        user = StudentUser.objects.get(email=request.user)
    is_first = user.is_first

    # Get all liked colleges by requesr.user
    liked_col = Like.objects.filter(user1=request.user).order_by('-likeId')
    liked_colleges = list()
    for col in liked_col:
        liked_colleges = liked_colleges + list(chain(CollegeUser.objects.filter(collegeId=col.user2)))

    # Followed colleges
    followed_col = Followers.objects.filter(user1=request.user).order_by('-followId')
    followed_colleges = list()
    for col in followed_col:
        followed_colleges = followed_colleges + list(chain(CollegeUser.objects.filter(collegeId=col.user2)))

    # Getting highest ranked colleges by nirf
    nirf_colleges = CollegeUser.objects.exclude(nirfRanking=0).order_by('nirfRanking')

    data = {
        'liked_colleges': liked_colleges,
        'followed_colleges': followed_colleges,
        'nirf_colleges': nirf_colleges,
        'courses': Courses.objects.all(),
        'is_first': is_first,
        'group': group,
    }
    return render(request, 'home.html', data)

###################################
@login_required(login_url='signin')
def search(request):
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

        # Followed colleges
        followed_col = Followers.objects.filter(user1=request.user)[:4]
        followed_colleges = list()
        for col in followed_col:
            followed_colleges = followed_colleges + list(chain(CollegeUser.objects.filter(collegeId=col.user2)))

        # Get all liked colleges by requesr.user
        liked_col = Like.objects.filter(user1=request.user)[:4]
        liked_colleges = list()
        for col in liked_col:
            liked_colleges = liked_colleges + list(chain(CollegeUser.objects.filter(collegeId=col.user2)))
            
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
def account(request):
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
            if review.get('studentId') in student_list:
                continue
            else:
                college_reviewed_users = college_reviewed_users + list(chain(StudentUser.objects.filter(studentId=review.get('studentId_id'))))
                student_list.append(review.get('studentId'))

        CourseReviews =  CourseReview.objects.filter(collegeId=user_obj).order_by('-date')
        courseReviews_tmp = CourseReview.objects.filter(collegeId=user_obj).values()
        course_reviewed_users = list()
        student_list = list()
        for review in courseReviews_tmp:
            if review.get('studenId') in student_list:
                continue
            else:
                course_reviewed_users = course_reviewed_users + list(chain(StudentUser.objects.filter(studentId=review.get('studentId_id'))))
                student_list.append(review.get('studenId'))

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
        }
    if group == 'student':
        user_obj = StudentUser.objects.get(email=request.user)
        posts = Images.objects.filter(userId=request.user).order_by('-imageId')
        postCount = Images.objects.filter(userId=request.user).count()
        liked = ImageLikes.objects.filter(userId=request.user).values()
        ids = list()
        for like in liked:
            ids.append(like.get('imageId_id'))

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
    username = str(username)
    group = str(group)

    if group == 'college':
        user = CollegeUser.objects.get(username=username)

        if user.email == request.user.email:
            return redirect('institute-account')

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
                college_courses = college_courses + list(chain(Courses.objects.filter(courseId=course.get('courseId_id'))))

            posts = Images.objects.filter(userId=college.id).order_by('-imageId')
            postCount = Images.objects.filter(userId=college.id).count()

            likedposts = ImageLikes.objects.filter(userId=request.user).values()
            ids = list()
            for like in likedposts:
                ids.append(like.get('imageId_id'))

            collegeReviews = CollegeReview.objects.filter(collegeId=college.id).order_by('-date')
            collegeReviews_tmp = CollegeReview.objects.filter(collegeId=college.id).values()
            college_reviewed_users = list()
            student_list = list()
            for review in collegeReviews_tmp:
                if review.get('studentId') in student_list:
                    continue
                else:
                    college_reviewed_users = college_reviewed_users + list(chain(StudentUser.objects.filter(studentId=review.get('studentId_id'))))
                    student_list.append(review.get('studentId'))

            CourseReviews =  CourseReview.objects.filter(collegeId=college.id).order_by('-date')
            courseReviews_tmp = CourseReview.objects.filter(collegeId=college.id).values()
            course_reviewed_users = list()
            student_list = list()
            for review in courseReviews_tmp:
                if review.get('studenId') in student_list:
                    continue
                else:
                    course_reviewed_users = course_reviewed_users + list(chain(StudentUser.objects.filter(studentId=review.get('studentId_id'))))
                    student_list.append(review.get('studenId'))

            visiting_user_group = None
            if request.user.groups.exists():
                visiting_user_group = request.user.groups.all()[0].name

            data = {
                'liked': liked,
                'followed': followed,
                'user': user,
                'college_courses': college_courses,
                'type': 'college',
                'posts': posts,
                'postCount': postCount,
                'ids': ids,
                'collegeReviews': collegeReviews,
                'CourseReviews': CourseReviews,
                'college_reviewed_users': college_reviewed_users,
                'course_reviewed_users': course_reviewed_users,
                'visiting_user_group': visiting_user_group,
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

            posts = Images.objects.filter(userId=student.id).order_by('-imageId')
            postCount = Images.objects.filter(userId=student.id).count()

            likedposts = ImageLikes.objects.filter(userId=request.user).values()
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
                        Like(user1=user, user2=user, date=datetime.now().date()).save()
                    elif request.POST.get('purpose') == 'self-dislike':
                        Like.objects.filter(user1=user, user2=user).delete()
                    like_count = Like.objects.filter(user2=user).count()
                    if group == 'college':
                        CollegeUser.objects.filter(email=request.user).update(profileLikes=like_count)
                    elif group == 'student':
                        StudentUser.objects.filter(email=request.user).update(profileLikes=like_count)
                    msg = { 'success': True, 'count': like_count, }
                    return JsonResponse(msg)
                except ValidationError:
                    msg = { 'success': False, }
                    return JsonResponse(msg)
    if request.method == 'GET':
        userid = str(request.GET.get('userid'))
        purpose = str(request.GET.get('purpose'))
        acctype = str(request.GET.get('acctype'))
        try:
            user = User.objects.get(email=userid)
            if purpose == 'like':
                Like(user1=request.user, user2=user, date=datetime.now().date()).save()
            elif purpose == 'dislike':
                Like.objects.filter(user1=request.user, user2=user).delete()
            like_count = Like.objects.filter(user2=user).count()
            if acctype == 'college':
                CollegeUser.objects.filter(email=userid).update(profileLikes=like_count)
            elif acctype == 'student':
                StudentUser.objects.filter(email=userid).update(profileLikes=like_count)
            msg = { 'success': True, 'count': like_count, }
            return JsonResponse(msg)
        except ValidationError:
            msg = { 'success': False }
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

@login_required(login_url='signin')
# Follow or to Unfollow
def follow_unfollow(request):
    userid = str(request.GET.get('userid'))
    purpose = str(request.GET.get('purpose'))
    acctype = request.GET.get('acctype')

    try:
        user = User.objects.get(email=userid)
        if purpose == 'follow':
            Followers(user1=request.user, user2=user, date=datetime.now().date()).save()
        elif purpose == 'unfollow':
            Followers.objects.filter(user1=request.user, user2=user).delete()
        follow_count = Followers.objects.filter(user2=user).count()
        if acctype == 'college':
            CollegeUser.objects.filter(email=userid).update(profileFollowers=follow_count)
        elif acctype == 'student':
            StudentUser.objects.filter(email=userid).update(profileFollowers=follow_count)
        msg = { 'success': True, 'count': follow_count, }
    except ValidationError:
        msg = { 'success': False }

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
                msg = { 'success': False }
                return JsonResponse(msg)

##############################
def student_signup(request):
    data = {
        'cities': Cities.objects.all(),
        'courses': Courses.objects.all(),
    }
    return render(request, 'student-signup.html', data)


####################################
def submit_student_signup(request):
    if request.method == 'POST':
        profile = request.FILES.get('profile')
        backprof = request.FILES.get('backprof')
        name = request.POST.get('firstname')
        surname = request.POST.get('lastname')
        description = request.POST.get('profileDescription') 
        # profileDescription is from student-signup.html (id='profileDescription')
        location = request.POST.get('location')
        courses = request.POST.getlist('courses')
        username = request.POST.get('username')
        email = request.POST.get('email')
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

                msg = { 'success': True }
                return JsonResponse(msg)
            except (ValidationError):
                msg = { 'success': False }
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
        url = request.POST.get('post-url')
        date = datetime.now()

        try:
            user_obj = User.objects.get(username=request.user)
            post = Images(userId=user_obj, image=image, title=description, url=url, date=date)
            post.save()
            msg = {'success': True,}
        except ValidationError:
            msg = {'success': False,}
        return JsonResponse(msg)

@login_required(login_url='signin')
def submit_college_review(request):
    if request.method == 'POST':
        text = request.POST.get('college-review')
        campus_rating = int(request.POST.get('campus-input'))
        library_rating = int(request.POST.get('library-input'))
        userid = str(request.POST.get('userid'))
        college = CollegeUser.objects.get(email=userid)
        student = StudentUser.objects.get(email=request.user.email)
        try:
            total_rating = int((campus_rating+library_rating)/2)

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
                total = int(totalsum / totalcount)
            elif campus is None and library is None and total is not None or campus == 0 and library == 0 and total != 0:
                campus = int(campus_rating)
                campussum = campus
                library = int(library_rating)
                librarysum = library
                reviewcount = 1
                 
                totalsum = int(totalsum + (campus + library))
                totalcount = totalcount + 2
                total = int(totalsum / totalcount)
            elif campus is not None and library is not None or campus != 0 and library != 0:
                campussum = campussum + campus
                reviewcount = reviewcount + 1
                campus = int(campussum / reviewcount)
                librarysum = librarysum + library
                library = int(librarysum / reviewcount)
                totalsum = int(totalsum + (campus + library))
                totalcount = totalcount + 2
                total = int(totalsum / totalcount)
            else:
                raise ValidationError

            count = CollegeReview.objects.filter(collegeId_id=college).count() + CourseReview.objects.filter(collegeId_id=college).count()
            CollegeUser.objects.filter(email=userid).update(reviewCount=count, campusRating=campus, libraryRating=library,
            totalRating=total, campusSum=campussum, librarySum=librarysum, collegeReviewCount=reviewcount, totalSum=totalsum, totalCount=totalcount)
            msg = { 'success': True, }
        except ValidationError:
            msg = { 'success': False, }
        return JsonResponse(msg)

@login_required(login_url='signin')
def submit_course_review(request):
    if request.method == 'POST':
        courseid = int(request.POST.get('select-course'))
        text = str(request.POST.get('course-review-text'))
        staff_rating = int(request.POST.get('staff-input'))
        curriculum_rating = int(request.POST.get('curriculum-input'))
        userid = str(request.POST.get('userid'))

        course = CollegeCourses.objects.get(collegecourseId=courseid)
        college = CollegeUser.objects.get(email=userid)
        student = StudentUser.objects.get(email=request.user.email)
        try:
            total_rating = int((staff_rating+curriculum_rating)/2)

            CourseReview(courseId=course, collegeId=college, studentId=student, message=text,
            staffRating = staff_rating, curriculumRating=staff_rating, date=datetime.now(), totalRating=total_rating).save()

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
                total = int(totalsum / totalcount)
            elif staff is None and curriculum is None and total is not None or staff == 0 and curriculum == 0 and total != 0:
                staff = int(staff_rating)
                staffsum = staff
                curriculum = int(curriculum_rating)
                curriculumsum = curriculum
                reviewcount = 1

                totalsum = int(totalsum + (staff + curriculum))
                totalcount = totalcount + 2
                total = int(totalsum / totalcount)
            elif staff is not None and curriculum is not None or staff !=0 and curriculum != 0:
                staffsum = staffsum + staff
                reviewcount = reviewcount + 1
                staff = int(staffsum / reviewcount)
                curriculumsum = curriculumsum + curriculum
                curriculum = int(curriculumsum / reviewcount)
                totalsum = int(totalsum + (staff + curriculum))
                totalcount = totalcount + 2
                total = int(totalsum / totalcount)
            else:
                raise ValidationError

            CollegeCourses.objects.all().update(staffRating=staff, CurriculumRating=curriculum)
            count = CollegeReview.objects.filter(collegeId_id=college).count() + CourseReview.objects.filter(collegeId_id=college).count()
            CollegeUser.objects.filter(email=userid).update(reviewCount=count, totalRating=total, staffRating=staff,
            curriculumRating=curriculum, courseReviewCount=reviewcount, staffSum=staffsum, curriculumSum=curriculumsum)

            msg = { 'success': True, }
        except ValidationError:
            msg = { 'success': False, }
        
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