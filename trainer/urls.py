from . import views
from django.urls import path,include

urlpatterns = [

path('trainerdash/',views.Trainer_Dash,name='trainer_dashboard'),
path('studentdetails/',views.Student_Details,name='student_details'),
path('videoupload/',views.upload_videos,name='upload_videos'),
path('trainer_logout/',views.Trainer_logout,name='trainer_logout'),
path('student-progress/', views.Studentprogress_View, name='student_progress'),





]
