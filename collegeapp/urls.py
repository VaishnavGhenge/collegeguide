from os import name
from re import template
from django.contrib import auth
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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
    path('account/<int:id>/', views.account, name='account2'),

    path('account/<str:group>/<str:username>/',
         views.view_account, name='visit-account'),

    path('likedislike/', views.likedislike, name='likedislike'),
    path('likedislikePosts/', views.likedislikePosts, name='likedislikePosts'),

    path('follow_unfollow/', views.follow_unfollow, name='follow_unfollow'),

    path('institute-signup/', views.institute_signup, name='institute-signup'),
    path('submit-institute-signup/', views.submit_institute_signup,
         name='submit-institute-signup'),
    path('institute-edit/', views.institute_edit, name='institute-edit'),

    path('student-signup/', views.student_signup, name='student-signup'),
    path('submit-student-signup/', views.submit_student_signup,
         name='submit-student-signup'),
    path('student-edit/', views.student_edit, name='student-edit'),

    path('courses_submit/', views.courses_submit, name='courses_submit'),
    path('submit-institute-post/', views.submit_institute_post,
         name='submit-institute-post'),
    path('submit-college-review/', views.submit_college_review,
         name='submit-college-review'),
    path('submit-course-review/', views.submit_course_review,
         name='submit-course-review'),

    path('check/', views.check, name='check'),
    path('check-email/', views.check_email, name='check-email'),
    path('sendotp/', views.sendOTP, name='sendotp'),
    path('checkotp/', views.checkotp, name='checkotp'),
    path('clearsession/', views.clearsession, name='clearsession'),
    path('getratingstats/', views.getratingstats, name='getratingstats'),
    path('helpful-action/', views.helpful_view, name='helpful-view'),

    path('page/<str:course>/', views.courseview_pre, name='courseview-pre'),

    path('admin/dashboard/', views.dashboard, name='dashboard'),
    path('admin/dashboard/<int:id>/', views.dashboard, name='dashboard2'),
    path('admin/forms/', views.admin_forms, name='admin-forms'),
    path('edit-rank/', views.editRank, name='edit-rank'),
    path('admin/forms/<str:type>/<int:id>', views.admin_forms, name='admin-forms2'),

    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    path('404/', views.errorcode404, name='404'),
    path('500/', views.errorcode500, name='500'),
]
