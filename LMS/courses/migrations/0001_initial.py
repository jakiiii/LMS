# Generated by Django 2.2 on 2020-07-17 11:59

import ckeditor.fields
import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import lms.utils_file


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        ('instructor', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(blank=True, max_length=10, unique=True)),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Course Title')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('course_short_description', models.TextField(blank=True, max_length=200, null=True, verbose_name='Course details')),
                ('course_long_description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('will_learn', ckeditor.fields.RichTextField()),
                ('course_image', models.FileField(default='assets/default_images/no-image.png', upload_to=lms.utils_file.upload_image_path)),
                ('course_intro_video', models.FileField(blank=True, max_length=500, null=True, upload_to=lms.utils_file.upload_image_path)),
                ('course_intro_video_duration', models.CharField(blank=True, max_length=20, null=20)),
                ('course_complete_duration', models.CharField(max_length=10, verbose_name='Duration')),
                ('course_for', models.CharField(choices=[('beginner', ' BEGINNER'), ('intermediate', 'INTERMEDIATE'), ('advance', 'ADVANCED')], default='Select For', max_length=20)),
                ('file', models.FileField(blank=True, null=True, upload_to=lms.utils_file.upload_image_path)),
                ('active', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
                ('locked', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.Category')),
                ('instructor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.Subcategory')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Lessons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Lessons title')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('description', models.TextField(blank=True, max_length=800, null=True)),
                ('lesson_file', models.FileField(blank=True, null=True, upload_to='')),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('course_of', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_lesson', to='courses.Courses')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('video', models.FileField(upload_to=lms.utils_file.upload_image_path)),
                ('duration', models.CharField(max_length=10, verbose_name='Duration')),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('active', models.BooleanField(default=True)),
                ('locked', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('episode_instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.Instructor')),
                ('lesson_of', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episode_lesson', to='courses.Courses')),
                ('series_of', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episode_series', to='courses.Lessons')),
            ],
            options={
                'verbose_name': 'Episodes',
                'verbose_name_plural': 'Episodes',
                'ordering': ['created_at'],
            },
        ),
    ]
