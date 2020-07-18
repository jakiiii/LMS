from django import forms
from django.utils import timezone

from .models import Instructor, Education, Experience, Certification, CompanySettings
from courses.models import Courses, Lessons, Episode
from blog.models import Blog


# Create your form here.
class DateInput(forms.DateInput):
    input_type = 'date'


class CreateBlogPostFrom(forms.ModelForm):

    class Meta:
        model = Blog
        fields = [
            'title',
            'cover_image',
            'video',
            'content',
            'tags',
            'active',
        ]

        labels = {
            'title': 'Title',
            'cover_image': 'Cover Image',
            'video': 'Video',
            'content': 'Content',
            'tags': 'Tags',
            'active': 'Active',
        }


class CreateCourseForm(forms.ModelForm):
    active = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(attrs={'style': 'width:1.5rem; height:1.5rem;'}))
    featured = forms.BooleanField(initial=False, required=False, widget=forms.CheckboxInput(attrs={'style': 'width:1.5rem; height:1.5rem;'}))
    locked = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(attrs={'style': 'width:1.5rem; height:1.5rem;'}))

    class Meta:
        model = Courses
        fields = [
            'title',
            'price',
            'course_short_description',
            'course_long_description',
            'will_learn',
            'course_image',
            'course_intro_video',
            'course_intro_video_duration',
            'course_complete_duration',
            'course_for',
            'category',
            'subcategory',
            'file',
            'active',
            'featured',
            'locked',
        ]
        labels = {
            'title': 'Title',
            'price': 'Price',
            'course_short_description': 'Lessons Short Description',
            'course_long_description': 'Lessons Long Description',
            'will_learn': 'What you\'ll learn',
            'course_image': 'Lessons Image',
            'course_intro_video': 'Lessons Intro Video',
            'course_intro_video_duration': 'Lessons Intro Video Duration',
            'course_complete_duration': 'Lessons Complete Duration',
            'course_for': 'Lessons For',
            'category': 'Category',
            'subcategory': 'Subcategory',
            'file': 'File',
            'active': 'Active',
            'featured': 'Featured',
            'locked': 'Locked',
        }


class InstructorCreationForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = (
            'first_name',
            'last_name',
            'designation',
            'commission',
            'short_bio',
            'long_bio',
            'address',
            'address_office',
            'school',
            'college',
            'university',
            'phd',
            'language',
            'email',
            'phone',
            'image',
            'facebook',
            'twitter',
            'linkedin',
        )
        labels = {
            'first_name': 'Fist Name',
            'last_name': 'Last Name',
            'designation': 'Designation',
            'commission': 'Commission(%)',
            'short_bio': 'Short Bio',
            'long_bio': 'Long Bio',
            'address': 'Home Address',
            'address_office': 'Office Address',
            'school': 'School',
            'college': 'College',
            'university': 'University',
            'phd': 'PHD',
            'language': 'Language',
            'email': 'Email',
            'phone': 'Phone No',
            'image': 'Image',
            'facebook': 'Facebook',
            'twitter': 'Twitter',
            'linkedin': 'Linkedin',
        }


class EducationCreationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = (
            'professor',
            'title',
            'Institute_name',
            'from_date',
            'to_date'
        )
        widgets = {
            'from_date': DateInput(),
            'to_date': DateInput(),
        }
        labels = {
            'professor': 'Professor',
            'title': 'Certificate Name',
            'Institute_name': 'Institute Name',
            'from_date': 'From Date',
            'To Date': 'To Date'
        }


class CertificationCreationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = (
            'professor',
            'title',
            'certification_description',
            'period',
            'ex_end_period'
        )
        widgets = {
            'period': DateInput(),
            'ex_end_period': DateInput(),
        }
        labels = {
            'professor': 'Professor',
            'title': 'Certification Name',
            'certification_description': 'Certification Description',
            'period': 'Issue Date',
            'ex_end_period': 'Expire End',
        }


class ExperienceCreationForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = (
            'professor',
            'title',
            'experience_description',
            'ex_period',
            'ex_end_period'
        )
        widgets = {
            'ex_period': DateInput(),
            'ex_end_period': DateInput(),
        }
        labels = {
            'professor': 'Professor',
            'title': 'Experience Title',
            'experience_description': 'Experience Description',
            'ex_period': 'From Date',
            'ex_end_period': 'To Date',
        }


class LessonsCreationForm(forms.ModelForm):
    active = forms.BooleanField(initial=True, required=False,
                                widget=forms.CheckboxInput(attrs={'style': 'width:1.5rem; height:1.5rem;'}))

    class Meta:
        model = Lessons
        fields = [
            'course_of',
            # 'lesson_title',
            'description',
            # 'lessons_video',
            # 'lessons_video_duration',
            # 'lesson_file',
            # 'lesson_price',
            'active',
            # 'is_locked',
        ]
        labels = {
            'course_of': 'Lesson Of',
            # 'lesson_title': 'Series Title',
            'description': 'Description',
            # 'lessons_video': 'Series Video',
            # 'lessons_video_duration': 'Series Video Duration',
            # 'lesson_file': 'Series File',
            # 'lesson_price': 'Series Price',
            'active': 'Active',
            # 'is_locked': 'Is_Locked',
        }


class EpisodeCreationForm(forms.ModelForm):
    active = forms.BooleanField(initial=True, required=False,
                                widget=forms.CheckboxInput(attrs={'style': 'width:1.5rem; height:1.5rem;'}))
    locked = forms.BooleanField(initial=True, required=False,
                                widget=forms.CheckboxInput(attrs={'style': 'width:1.5rem; height:1.5rem;'}))

    class Meta:
        model = Episode
        fields = [
            'episode_instructor',
            'lesson_of',
            'series_of',
            'title',
            'video',
            'duration',
            'price',
            'active',
            'locked',
        ]
        labels = {
            'episode_instructor': 'Instructor',
            'lesson_of': 'Lesson of',
            'series_of': 'Series of',
            'title': 'Title',
            'video': 'Video',
            'duration': 'Video Duration',
            'price': 'Episode Price',
            'active': 'Active',
            'locked': 'Locked',
        }

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['series_of'].queryset = Lessons.objects.none()
        #
        #     if 'lesson_of' in self.data:
        #         try:
        #             lesson_of_id = int(self.data.get('lesson_of'))
        #             self.fields['series_of'].queryset = Lessons.objects.filter(lesson_of_id=lesson_of_id).order_by('lesson_title')
        #         except (ValueError, TypeError):
        #             pass  # invalid input from the client; ignore and fallback to empty City queryset
        #     elif self.instance.slug:
        #         self.fields['series_of'].queryset = self.instance.lesson_of.series_of_set.order_by('title')


class CompanySettingsCreationForm(forms.ModelForm):
    class Meta:
        model = CompanySettings
        fields = [
            'company_name',
            'company_address',
            'company_email',
            'vat_registration_number',
            'vat_percentage'
        ]
        labels = {
            'company_name': 'Company Name',
            'company_address': 'Company Address',
            'company_email': 'Company Email',
            'vat_registration_number': 'VAT Registration Number',
            'vat_percentage': 'VAT Percentage'
        }
