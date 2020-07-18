from django.urls import path
from . import views
from .views import (
    InstructorProfileView,

    InstructorManageBlog,
    InstructorBlogPostCreateView,
    InstructorBlogUpdateView,
    InstructorBlogDeleteView,

    ManageLessonListView,
    ManageLessonCreateView,
    SeriesUpdateView,
    SeriesDeleteView,

    ManageEpisodeView,
    EpisodeCreateView,
    UpdateEpisodeView,
    DeleteEpisodeView,

    InstructorManageCourse,
    InstructorCourseCreateView,
    InstructorCourseUpdateView,
    InstructorCourseDeleteView,

    EducationManageView,
    EducationCreateView,
    EducationUpdateView,
    EducationDeleteView,

    InstructorManageView,
    NewInstructorCreateView,
    InstructorUpdateView,
    InstructorDeleteView,

    CertificationManageView,
    CertificationCreateView,
    CertificationUpdateView,
    CertificationDeleteView,

    ExperienceManageView,
    ExperienceCreateView,
    ExperienceUpdateView,
    ExperienceDeleteView,

    CompanySettingListView,
    CompanySettingCreateView,
    CompanySettingUpdateView,
    CompanySettingDeleteView,

    StudentAdminListView,
    StudentAdminUpdateView,
    StudentAdminDeleteView,
    invoice_details,
    invoice_list,
    settings
)

urlpatterns = [
    path('', InstructorProfileView.as_view(), name='instructor-dashboard'),

    path('instructor_blog/', InstructorManageBlog.as_view(), name='instructor-blog'),
    path('create_blog/', InstructorBlogPostCreateView.as_view(), name='create-blog-post'),
    path('blog/update/<slug:slug>/', InstructorBlogUpdateView.as_view(), name='update-blog-post'),
    path('blog/delete/<slug:slug>/', InstructorBlogDeleteView.as_view(), name='delete-blog-post'),

    path('instructor_courses/', InstructorManageCourse.as_view(), name='instructor-courses'),
    path('create_courses/', InstructorCourseCreateView.as_view(), name='create-courses'),
    path('course/update/<slug:slug>/', InstructorCourseUpdateView.as_view(), name='update-courses'),
    path('course/delete/<slug:slug>/', InstructorCourseDeleteView.as_view(), name='delete-courses'),

    path('manage/lesson/', ManageLessonListView.as_view(), name='manage-lesson'),
    path('create/lesson/', ManageLessonCreateView.as_view(), name='create-lesson'),
    path('update/lesson/<slug:slug>/', SeriesUpdateView.as_view(), name='update-series'),
    path('delete/lesson/<slug:slug>/', SeriesDeleteView.as_view(), name='delete-lesson'),

    path('manage/episode/', ManageEpisodeView.as_view(), name='manage-episode'),
    path('create/episode/', EpisodeCreateView.as_view(), name='create-episode'),
    path('update/episode/<slug:slug>/', UpdateEpisodeView.as_view(), name='update-episode'),
    path('delete/episode/<slug:slug>/', DeleteEpisodeView.as_view(), name='delete-episode'),

    path('manage/', InstructorManageView.as_view(), name='instructor-manage'),
    path('new/add/', NewInstructorCreateView.as_view(), name='instructor-create'),
    path('update/<slug:slug>/', InstructorUpdateView.as_view(), name='instructor-update'),
    path('delete/<slug:slug>/', InstructorDeleteView.as_view(), name='professor-delete'),

    path('education/manage/', EducationManageView.as_view(), name='education-manage'),
    path('education/create/', EducationCreateView.as_view(), name='education-create'),
    path('education/update/<slug:slug>/', EducationUpdateView.as_view(), name='education-update'),
    path('education/delete/<slug:slug>/', EducationDeleteView.as_view(), name='education-delete'),

    path('certification/manage/', CertificationManageView.as_view(), name='certification-manage'),
    path('certification/create/', CertificationCreateView.as_view(), name='certification-create'),
    path('certification/update/<slug:slug>/', CertificationUpdateView.as_view(), name='certification-update'),
    path('certification/delete/<slug:slug>/', CertificationDeleteView.as_view(), name='certification-delete'),

    path('experience/manage/', ExperienceManageView.as_view(), name='experience-manage'),
    path('experience/create/', ExperienceCreateView.as_view(), name='experience-create'),
    path('experience/update/<slug:slug>/', ExperienceUpdateView.as_view(), name='experience-update'),
    path('experience/delete/<slug:slug>/', ExperienceDeleteView.as_view(), name='experience-delete'),

    path('company/settings/', CompanySettingListView.as_view(), name='company-settings'),
    path('company/settings/create/', CompanySettingCreateView.as_view(), name='company-settings-create'),
    path('company/settings/update/<slug:slug>/', CompanySettingUpdateView.as_view(), name='company-settings-update'),
    path('company/settings/delete/<slug:slug>/', CompanySettingDeleteView.as_view(), name='company-settings-delete'),

    path('manage/student/', StudentAdminListView.as_view(), name='manage-student-admin'),
    path('update/student/<slug:slug>/', StudentAdminUpdateView.as_view(), name='update-user-admin'),
    path('delete/student/<slug:slug>/', StudentAdminDeleteView.as_view(), name='delete-user'),

    # --------- function based view for reports --------------#
    path('report/category_professor', views.category_professor, name='category_professor'),
    path('report/top_sales_videos_professor', views.top_sales_videos_professor, name='top_sales_videos_professor'),
    path('report/top_paid_videos_professor', views.top_paid_videos_professor, name='top_paid_videos_professor'),
    path('report/top_private_lesson_contact_professor', views.top_private_lesson_contact_professor, name='top_private_lesson_contact_professor'),
    path('report/top_viewing_professor', views.top_viewing_professor, name='top_viewing_professor'),
    path('report/top_self_professor', views.top_self_professor, name='top_self_professor'),
    path('report/fewer_videos_professor', views.fewer_videos_professor, name='fewer_videos_professor'),
    path('report/sales', views.sales, name='sales'),
    path('report/series_wise_sales_report', views.series_wise_sales_report, name='series_wise_sales_report'),
    path('report/professor_wise_sales_report', views.professor_wise_sales_report, name='professor_wise_sales_report'),

    # ------------ function based view for invocie ------#
    path('instructor_invoice/', invoice_list, name='instructor_invoice'),
    path('instructor_invoice/details/<key>', invoice_details, name='instructor_invoice_details'),


    # ---------- company settings ____________ #
    path('settings/', settings, name='settings'),

]
