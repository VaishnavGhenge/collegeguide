from math import nan
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('submit-contact/', views.submit_contact, name='submit-contact'),
    path('submit-email/', views.submit_email, name='submit-email'),

    path('signin/', views.signin, name='signin'),
    path('submit-signin/', views.submit_signin, name='submit-signin'),
    path('logout/', views.user_logout, name='logout'),

    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('account/', views.account, name='account'),

    path('account/<str:group>/<str:username>/', views.view_account, name='visit-account'),

    path('likedislike/', views.likedislike, name='likedislike'),
    path('likedislikePosts/', views.likedislikePosts, name='likedislikePosts'),

    path('follow_unfollow/', views.follow_unfollow, name='follow_unfollow'),

    path('institute-signup/', views.institute_signup, name='institute-signup'),
    path('submit-institute-signup/', views.submit_institute_signup, name='submit-institute-signup'),

    path('student-signup/', views.student_signup, name='student-signup'),
    path('submit-student-signup/', views.submit_student_signup, name='submit-student-signup'),

    path('courses_submit/', views.courses_submit, name='courses_submit'),
    path('submit-institute-post/', views.submit_institute_post, name='submit-institute-post'),
    path('submit-college-review/', views.submit_college_review, name='submit-college-review'),
    path('submit-course-review/', views.submit_course_review, name='submit-course-review'),
    
    path('check/', views.check, name='check'),
    path('check-email/', views.check_email, name='check-email'),
    path('sendotp/', views.sendOTP, name='sendotp'),
    path('checkotp/', views.checkotp, name='checkotp'),
    path('clearsession/', views.clearsession, name='clearsession'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('404/', views.errorcode404, name='404'),
]