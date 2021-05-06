# Generated by Django 3.1.7 on 2021-05-04 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CollegeUser',
            fields=[
                ('collegeId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('username', models.CharField(max_length=200, null=True)),
                ('name', models.CharField(max_length=200)),
                ('profileImage', models.ImageField(default='user/avatar.png', upload_to='user/college/profile/')),
                ('backgroundImage', models.ImageField(default='user/default-back.jpeg', upload_to='user/college/backprofile')),
                ('profileFollowers', models.IntegerField(default=0)),
                ('profileLikes', models.IntegerField(default=0)),
                ('profileDescription', models.CharField(max_length=300, null=True)),
                ('profileWebsite', models.CharField(max_length=200, null=True)),
                ('courseCount', models.IntegerField(default=0)),
                ('profileVisits', models.IntegerField(default=0)),
                ('imageCount', models.IntegerField(default=0)),
                ('postCount', models.IntegerField(default=0)),
                ('campusRating', models.PositiveSmallIntegerField(null=True)),
                ('libraryRating', models.PositiveSmallIntegerField(null=True)),
                ('verified', models.BooleanField(default=False)),
                ('reviewCount', models.IntegerField(default=0)),
                ('location', models.CharField(max_length=200)),
                ('postalcode', models.IntegerField(null=True)),
                ('collegeFoundation', models.DateField()),
                ('alumniCount', models.IntegerField(default=0)),
                ('college_type', models.CharField(max_length=100)),
                ('college_foundation_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('contactId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('courseId', models.AutoField(primary_key=True, serialize=False)),
                ('courseName', models.CharField(max_length=200)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='PLatformStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platformVisitors', models.IntegerField(default=0)),
                ('studentUsers', models.IntegerField(default=0)),
                ('collegeUsers', models.IntegerField(default=0)),
                ('totalReviews', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='StudentUser',
            fields=[
                ('studentId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('profileImage', models.ImageField(default='user/avatar.png', upload_to='user/student/profile/')),
                ('backgroundImage', models.ImageField(default='user/default-back.jpeg', upload_to='user/student/backprofile/')),
                ('prefCourse1', models.CharField(max_length=100, null=True)),
                ('prefCourse2', models.CharField(max_length=100, null=True)),
                ('prefCourse3', models.CharField(max_length=100, null=True)),
                ('prefLocation', models.CharField(max_length=200, null=True)),
                ('prefInstitute', models.CharField(max_length=200, null=True)),
                ('profileFollowers', models.IntegerField(default=0)),
                ('profileDescription', models.CharField(max_length=300, null=True)),
                ('profileWebsite', models.CharField(max_length=100, null=True)),
                ('profileVisits', models.IntegerField(default=0)),
                ('postCount', models.IntegerField(default=0)),
                ('reviewCount', models.IntegerField(default=0)),
                ('profileLikes', models.IntegerField(default=0)),
                ('reviewPoints', models.IntegerField(default=0)),
                ('is_alumni', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CollegeCourses',
            fields=[
                ('courseId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='collegeapp.courses')),
                ('name', models.CharField(max_length=200)),
                ('courseRating', models.PositiveSmallIntegerField(null=True)),
                ('instrumentAvailabilityRating', models.PositiveSmallIntegerField(null=True)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collegeapp.collegeuser')),
            ],
        ),
        migrations.CreateModel(
            name='UserPosts',
            fields=[
                ('postId', models.AutoField(primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=200)),
                ('message', models.CharField(max_length=400)),
                ('date', models.DateTimeField()),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('imageId', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(null=True, upload_to='user/image-posts/')),
                ('title', models.CharField(max_length=200, null=True)),
                ('location', models.CharField(max_length=300, null=True)),
                ('date', models.DateTimeField()),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CollegeReview',
            fields=[
                ('reviewId', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('message', models.CharField(max_length=400, null=True)),
                ('totalRating', models.PositiveSmallIntegerField(null=True)),
                ('campusRating', models.PositiveSmallIntegerField(null=True)),
                ('libraryRating', models.PositiveSmallIntegerField(null=True)),
                ('helpfulCount', models.IntegerField(default=0)),
                ('spamCount', models.IntegerField(default=0)),
                ('inappropriateCount', models.IntegerField(default=0)),
                ('collegeId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collegeapp.collegeuser')),
                ('studentId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collegeapp.studentuser')),
            ],
        ),
        migrations.CreateModel(
            name='CourseReview',
            fields=[
                ('reviewId', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('message', models.CharField(max_length=400)),
                ('totalRating', models.PositiveSmallIntegerField(null=True)),
                ('staffRating', models.PositiveSmallIntegerField(null=True)),
                ('curriculumRating', models.PositiveSmallIntegerField(null=True)),
                ('instrumentsRating', models.PositiveSmallIntegerField(null=True)),
                ('studentId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collegeapp.studentuser')),
                ('courseId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collegeapp.collegecourses')),
            ],
        ),
    ]
