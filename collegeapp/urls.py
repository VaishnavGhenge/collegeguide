from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('submit-contact/', views.submit_contact, name='submit-contact'),
    path('submit-email/', views.submit_email, name='submit-email'),

    path('signin/', views.signin, name='signin'),
    path('submit-signin/', views.submit_signin, name='submit-signin'),
    path('logout/', views.user_logout, name='logout'),

    path('institute-home/', views.institute_home, name='institute-home'),
    path('institute-search/', views.institute_search, name='institute-search'),
    path('institute-account/', views.institute_account, name='institute-account'),
    path('institute-signup/', views.institute_signup, name='institute-signup'),
    path('submit-institute-signup/', views.submit_institute_signup, name='submit-institute-signup'),
    path('courses_submit/', views.courses_submit, name='courses_submit'),
    path('check/', views.check, name='check'),
    path('check-email/', views.check_email, name='check-email'),

    path('404/', views.errorcode404, name='404'),
]