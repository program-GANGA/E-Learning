from . import views
from django.urls import path,include

urlpatterns = [

path('create_admin/', views.create_admin,name='create_admin'),
path('admin_dash/',views.admin_dash,name='admin_dashboard'),
path('addcourse/',views.add_course,name='add_course'),
path('logout/',views.admin_logout,name='logout'),
path('add_trainer/',views.add_trainer,name='add_trainer'),
path('student_progress/',views.admin_progress_view,name='admin_progressview'),
path('student_feedback/',views.admin_feedback_view,name='admin_feedbackview'),
path('tarinerrating/', views.trainerratings_view, name='trainer_rating'),
]
