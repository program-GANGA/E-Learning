from django.shortcuts import render,HttpResponse,redirect
from .models import Admin_Model,Trainer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from student.models import Course
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from student.models import VideoCompletion, User,StudentProfile,Feedback,TrainerRating
from trainer.models import RecordedVideo

def create_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
            return render(request, 'create_admin.html')
        try:
            user = User.objects.create_user(username=username, password=password)
            admin_account = Admin_Model.objects.create(user=user)
            return redirect('admin_dashboard')
        except IntegrityError:
            messages.error(request, 'An error occurred while creating the admin account.')
            return render(request, 'create_admin.html')

    return render(request, 'create_admin.html')


def admin_dash(request):
    return render(request,'admindash.html')

def add_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        fee = request.POST.get('fee')

        # Validation
        if not course_name or not fee:
            messages.error(request, 'Please fill in all fields.')
            return redirect('add_course')

        try:
            fee = float(fee) 
            if fee <= 0:
                messages.error(request, 'Fee must be a positive number.')
                return redirect('add_course')
        except ValueError:
            messages.error(request, 'Invalid fee value. Please enter a numeric value.')
            return redirect('add_course')
        
        if Course.objects.filter(name=course_name).exists():
            messages.error(request, 'Course already exists!') 
            return redirect('add_course')
        Course.objects.create(name=course_name, fee=fee)
        return redirect('admin_dashboard')

    return render(request, 'addcourse.html')

def add_trainer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        skype_id = request.POST.get('skype_id')
        whatsapp_number = request.POST.get('whatsapp_number')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        selected_course_id = request.POST.get('course')

        # Basic validation
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return redirect('add_trainer')

        user = User.objects.create_user(username=username, password=password)
        trainer = Trainer.objects.create(user=user, skype_id=skype_id, whatsapp_number=whatsapp_number,email=email,phone=phone)


        if selected_course_id:
            course = Course.objects.get(id=selected_course_id)
            trainer.courses.add(course)
        return redirect('admin_dashboard')

    courses = Course.objects.all()  
    return render(request, 'addtrainer.html', {'courses': courses})



def admin_progress_view(request):
    students = StudentProfile.objects.all()

    student_progress = []
    if not students.exists():
        context = {
            'student_progress': [],
            'message': 'No students registered yet.'
        }
    for student in students:
        total_videos = RecordedVideo.objects.filter(course=student.course).count()
        completed_videos = VideoCompletion.objects.filter(student=student.user, is_completed=True).count()
        if total_videos > 0:
            progress_percentage = (completed_videos / total_videos) * 100
        else:
            progress_percentage = 0
        
        student_progress.append({
            'student_name': student.name,
            'course_name': student.course.name if student.course else 'No course',
            'trainer_name': student.trainer.user.username if student.trainer else 'No trainer',
            'progress_percentage': int(progress_percentage),
        })

    context = {
        'student_progress': student_progress,
    }
    
    return render(request, 'adminprogressview.html', context)



def admin_feedback_view(request):
    feedbacks = Feedback.objects.select_related('student').all()  
    feedback_data = []

    for feedback in feedbacks:
        try:
            student_profile = StudentProfile.objects.get(user=feedback.student)
            course_name = student_profile.course.name if student_profile.course else 'No Course Assigned'
        except StudentProfile.DoesNotExist:
            course_name = 'No Course Assigned'
        
        feedback_data.append({
            'student_name': feedback.student.username, 
            'content': feedback.content,
            'created_at': feedback.created_at,
            'course_name': course_name,
        })

    return render(request, 'feedbackview.html', {'feedbacks': feedback_data})

def trainerratings_view(request):
    ratings = TrainerRating.objects.all().select_related('trainer', 'student')

    context = {
        'ratings': ratings
    }
    return render(request, 'ratingview.html', context)








    




def admin_logout(request):
    logout(request)  # Log the user out
    return redirect('login')






