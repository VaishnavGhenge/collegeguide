from django.db import models
from django.contrib.auth.models import User
from django.db.models.expressions import Col

######################################################################################################
# Contact and Email Form Models
class Contact(models.Model):
    contactId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.CharField(max_length=300)

class Email(models.Model):
    email = models.EmailField()

#####################################################################################################
# User Models
class StudentUser(models.Model):
    studentId = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    profileImage = models.ImageField(upload_to='user/student/profile/', default='user/avatar.png')
    backgroundImage = models.ImageField(upload_to='user/student/backprofile/', default='user/default-back.jpeg')
    prefCourse1 = models.CharField(max_length=100, null=True)
    prefCourse2 = models.CharField(max_length=100, null=True)
    prefCourse3 = models.CharField(max_length=100, null=True)
    prefLocation = models.CharField(max_length=200, null=True)
    prefInstitute = models.CharField(max_length=200, null=True)
    profileFollowers = models.IntegerField(default=0)
    profileDescription = models.CharField(max_length=300, null=True)
    profileWebsite = models.CharField(max_length=100, null=True)
    profileVisits =  models.IntegerField(default=0)
    postCount = models.IntegerField(default=0)
    reviewCount = models.IntegerField(default=0)
    profileLikes = models.IntegerField(default=0)
    reviewPoints = models.IntegerField(default=0)
    is_alumni = models.BooleanField(default=False)

class CollegeUser(models.Model):
    collegeId = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200)
    profileImage = models.ImageField(upload_to='user/college/profile/', default='user/avatar.png')
    backgroundImage = models.ImageField(upload_to='user/college/backprofile', default='user/default-back.jpeg')
    profileFollowers = models.IntegerField(default=0)
    profileLikes = models.IntegerField(default=0)
    profileDescription = models.CharField(max_length=300,null=True)
    profileWebsite = models.CharField(max_length=200, null=True)
    courseCount = models.IntegerField(default=0)
    profileVisits = models.IntegerField(default=0)
    imageCount = models.IntegerField(default=0)
    postCount = models.IntegerField(default=0)
    campusRating = models.PositiveSmallIntegerField(null=True)
    libraryRating = models.PositiveSmallIntegerField(null=True)
    verified = models.BooleanField(default=False)
    reviewCount = models.IntegerField(default=0)
    location = models.CharField(max_length=200)
    postalcode = models.IntegerField(null=True)
    alumniCount = models.IntegerField(default=0)
    college_type = models.CharField(max_length=100)
    college_foundation_date = models.DateField()

##########################################################################################
# User Post Models
class Images(models.Model):
    imageId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user/image-posts/', null=True)
    title = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=300, null=True)
    date = models.DateTimeField()

class UserPosts(models.Model):
    postId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    message = models.CharField(max_length=400)
    date = models.DateTimeField()

############################################################################################
# Other Supporting Models
class Courses(models.Model):
    courseId = models.AutoField(primary_key=True)
    courseName = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self):
        return self.courseName

class CollegeCourses(models.Model):
    courseId = models.OneToOneField(Courses, on_delete=models.CASCADE, primary_key=True)
    userId = models.ForeignKey(CollegeUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    courseRating = models.PositiveSmallIntegerField(null=True)
    instrumentAvailabilityRating = models.PositiveSmallIntegerField(null=True)

class AlumniStudentCollege():
    id = models.AutoField(primary_key=True)
    studentId = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    collegeId = models.ForeignKey(CollegeUser, on_delete=models.CASCADE)

########################################################################################
# User Review Models
class CollegeReview(models.Model):
    reviewId = models.AutoField(primary_key=True)
    collegeId = models.ForeignKey(CollegeUser, on_delete=models.CASCADE)
    studentId = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    date = models.DateTimeField()
    message = models.CharField(max_length=400, null=True)
    totalRating = models.PositiveSmallIntegerField(null=True)
    campusRating = models.PositiveSmallIntegerField(null=True)
    libraryRating = models.PositiveSmallIntegerField(null=True)
    helpfulCount = models.IntegerField(default=0)
    spamCount = models.IntegerField(default=0)
    inappropriateCount = models.IntegerField(default=0)

class CourseReview(models.Model):
    reviewId = models.AutoField(primary_key=True)
    courseId = models.ForeignKey(CollegeCourses, on_delete=models.CASCADE)
    studentId = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    date = models.DateTimeField()
    message = models.CharField(max_length=400)
    totalRating = models.PositiveSmallIntegerField(null=True)
    staffRating = models.PositiveSmallIntegerField(null=True)
    curriculumRating = models.PositiveSmallIntegerField(null=True)
    instrumentsRating = models.PositiveSmallIntegerField(null=True)

################################################################################################
# Website Statistics Models
class PLatformStatistics(models.Model):
    platformVisitors = models.IntegerField(default=0)
    studentUsers = models.IntegerField(default=0)
    collegeUsers = models.IntegerField(default=0)
    totalReviews = models.IntegerField(default=0)