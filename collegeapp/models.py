from datetime import date, datetime
from django.db import models
from django.contrib.auth.models import User

######################################################################################################
# Contact and Email Form Models


class Contact(models.Model):
    contactId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.CharField(max_length=300)
    date = models.DateTimeField(null=True)


class Email(models.Model):
    email = models.EmailField()

#####################################################################################################
# User Models


class StudentUser(models.Model):
    studentId = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    profileImage = models.ImageField(
        upload_to='user/student/profile/', default='user/avatar.png')
    backgroundImage = models.ImageField(
        upload_to='user/student/backprofile/', default='user/default-back.jpeg')
    prefCourse1 = models.CharField(max_length=100, null=True)
    prefCourse2 = models.CharField(max_length=100, null=True)
    prefCourse3 = models.CharField(max_length=100, null=True)
    prefLocation = models.CharField(max_length=200, null=True)
    profileFollowers = models.IntegerField(default=0)
    profileDescription = models.CharField(max_length=300, null=True)
    profileVisits = models.IntegerField(default=0)
    postCount = models.IntegerField(default=0)
    reviewCount = models.IntegerField(default=0)
    profileLikes = models.IntegerField(default=0)
    reviewPoints = models.IntegerField(default=0)
    is_alumni = models.BooleanField(default=False)
    is_first = models.BooleanField(default=False)


class CollegeUser(models.Model):
    collegeId = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField(default='')
    name = models.CharField(max_length=200)
    profileImage = models.ImageField(
        upload_to='user/college/profile/', default='user/avatar.png')
    backgroundImage = models.ImageField(
        upload_to='user/college/backprofile', default='user/default-back.jpeg')
    profileFollowers = models.IntegerField(default=0)
    profileLikes = models.IntegerField(default=0)
    profileDescription = models.CharField(max_length=300, null=True)
    profileWebsite = models.CharField(max_length=200, null=True)
    courseCount = models.IntegerField(default=0)
    profileVisits = models.IntegerField(default=0)
    imageCount = models.IntegerField(default=0)
    postCount = models.IntegerField(default=0)

    campusRating = models.PositiveSmallIntegerField(null=True)
    libraryRating = models.PositiveSmallIntegerField(null=True)
    collegeReviewCount = models.IntegerField(default=0)
    campusSum = models.IntegerField(default=0)
    librarySum = models.IntegerField(default=0)

    staffRating = models.PositiveSmallIntegerField(null=True)
    curriculumRating = models.PositiveSmallIntegerField(null=True)
    courseReviewCount = models.IntegerField(default=0)
    staffSum = models.IntegerField(default=0)
    curriculumSum = models.IntegerField(default=0)

    totalRating = models.PositiveSmallIntegerField(null=True)
    totalSum = models.IntegerField(default=0)
    totalCount = models.IntegerField(default=0)

    verified = models.BooleanField(default=False)
    reviewCount = models.IntegerField(default=0)
    city = models.CharField(max_length=200)
    postalcode = models.IntegerField(null=True)
    alumniCount = models.IntegerField(default=0)
    college_type = models.CharField(max_length=100)
    college_foundation_date = models.DateField()
    nirfRanking = models.IntegerField(default=0)
    is_first = models.BooleanField(default=False)

##########################################################################################
# User Post Models


class Images(models.Model):
    imageId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user/image-posts/', null=True)
    title = models.CharField(max_length=200, null=True)
    url = models.URLField(default='', null=True)
    totalLikes = models.IntegerField(default=0)
    location = models.CharField(max_length=300, null=True)
    date = models.DateTimeField()


class ImageLikes(models.Model):
    likeId = models.AutoField(primary_key=True)
    imageId = models.ForeignKey(Images, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

############################################################################################
# Other Supporting Models


class Courses(models.Model):
    courseId = models.AutoField(primary_key=True)
    courseName = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self):
        return self.courseName


class CollegeCourses(models.Model):
    collegecourseId = models.AutoField(primary_key=True)
    courseId = models.ForeignKey(Courses, on_delete=models.CASCADE)
    userId = models.ForeignKey(CollegeUser, on_delete=models.CASCADE)
    staffRating = models.PositiveSmallIntegerField(null=True)
    CurriculumRating = models.PositiveSmallIntegerField(null=True)


class AlumniStudentCollege():
    id = models.AutoField(primary_key=True)
    studentId = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    collegeId = models.ForeignKey(CollegeUser, on_delete=models.CASCADE)


class Cities(models.Model):
    citiId = models.AutoField(primary_key=True)
    cityName = models.CharField(max_length=200)
    nearCity = models.ForeignKey(
        'self', on_delete=models.PROTECT, null=True, default='')

    def __str__(self):
        return self.cityName


class Followers(models.Model):
    followId = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='one')
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='two')
    date = models.DateField()


class Like(models.Model):
    likeId = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='onelike')
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='twolike')
    date = models.DateField()

########################################################################################
# User Review Models


class CollegeReview(models.Model):
    reviewId = models.AutoField(primary_key=True)
    collegeId = models.ForeignKey(
        CollegeUser, on_delete=models.CASCADE, null=True)
    studentId = models.ForeignKey(
        StudentUser, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()
    message = models.CharField(max_length=700, null=True)
    totalRating = models.PositiveSmallIntegerField(null=True)
    campusRating = models.PositiveSmallIntegerField(null=True)
    libraryRating = models.PositiveSmallIntegerField(null=True)
    helpfulCount = models.IntegerField(default=0)
    notHelpfulCount = models.IntegerField(default=0)
    spamCount = models.IntegerField(default=0)
    inappropriateCount = models.IntegerField(default=0)
    is_alumni = models.BooleanField(default=False)


class CourseReview(models.Model):
    reviewId = models.AutoField(primary_key=True)
    courseId = models.ForeignKey(
        CollegeCourses, on_delete=models.CASCADE, null=True)
    collegeId = models.ForeignKey(
        CollegeUser, on_delete=models.CASCADE, null=True)
    studentId = models.ForeignKey(
        StudentUser, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()
    message = models.CharField(max_length=700)
    totalRating = models.PositiveSmallIntegerField(null=True)
    staffRating = models.PositiveSmallIntegerField(null=True)
    curriculumRating = models.PositiveSmallIntegerField(null=True)
    helpfulCount = models.IntegerField(default=0)
    notHelpfulCount = models.IntegerField(default=0)
    spamCount = models.IntegerField(default=0)
    inappropriateCount = models.IntegerField(default=0)
    is_alumni = models.BooleanField(default=False)


class Collegehelpful(models.Model):
    id = models.AutoField(primary_key=True)
    reviewid = models.ForeignKey(CollegeReview, on_delete=models.CASCADE)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    college = models.ForeignKey(
        CollegeUser, on_delete=models.CASCADE, null=True)
    purpose = models.CharField(max_length=50, null=True)


class Coursehelpful(models.Model):
    id = models.AutoField(primary_key=True)
    reviewid = models.ForeignKey(CourseReview, on_delete=models.CASCADE)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    college = models.ForeignKey(
        CollegeUser, on_delete=models.CASCADE, null=True)
    purpose = models.CharField(max_length=50, null=True)

################################################################################################
# Website Statistics Models


class PLatformStatistics(models.Model):
    id = models.AutoField(primary_key=True)
    platformVisitors = models.IntegerField(default=0)
    studentUsers = models.IntegerField(default=0)
    collegeUsers = models.IntegerField(default=0)
    totalCourses = models.IntegerField(default=0)
