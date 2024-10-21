from . import views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

path('',views.Home,name='home'),
path('studentregsiter/',views.StudentRegister,name='register'),
path('login/',views.user_login,name='login'),
path('dashboard/<int:video_id>/',views.DashBoard,name='student_dashboard'),
path('dashboard/', views.DashBoard, name='student_dashboard'), 
path('dashboard/<int:video_id>/', views.DashBoard, name='student_dashboard_with_video'), 
path('get-course-fee/<int:course_id>/', views.get_course_fee, name='get_course_fee'),
path('payment-success/', views.payment_success, name='payment_success'),
path('studentlogout',views.student_logout,name='logout'),
path('studentprofile/',views.student_profile,name='profile'),
path('trainerdetails/',views.Trainer_details,name='trainer_details'),
path('uploadedvideos/',views.Uploaded_Videos,name='Uploaded_Videos'),
path('progressview/',views.progress_view,name='progress_view'),
path('feedback',views.feedback_view,name='feedback'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
