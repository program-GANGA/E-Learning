from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from  adminapp.models import Trainer
from student.models import StudentProfile,Trainer,VideoCompletion,TrainerRating
from .models import *
from django.contrib.auth import logout
# Create your views here.

def Trainer_Dash(request):
    username = request.user.username
    return render(request,'trainerdash.html',{'username':username})


def Student_Details(request):

    trainer = Trainer.objects.get(user=request.user)

    # Get students with courses assigned to the trainer
    students = StudentProfile.objects.filter(course__in=trainer.courses.all())

    return render(request, 'studentdetails.html', {'students': students, 'trainer': trainer})




def upload_videos(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        video = request.FILES.get('video')
        trainer_profile = request.user.trainer  # Adjust based on how you access the trainer profile

        # Get all courses associated with the trainer
        courses = trainer_profile.courses.all()  # Fetch all related courses

        if courses.exists():  # Check if there are any associated courses
            course = courses.first()  # You can choose a specific course or implement a selection mechanism

            # Create and save the RecordedVideo instance
            recorded_video = RecordedVideo(title=title, video=video, course=course)
            recorded_video.save()

            return redirect('trainer_dashboard')
        else:
            return render(request, 'uploadvideos.html', {'error': 'Trainer is not associated with any course.'})
    return render(request, 'uploadvideos.html')




def Studentprogress_View(request):
    trainer = Trainer.objects.get(user=request.user)
    trainer_courses = trainer.courses.all()
    student_progress_list = []
    for course in trainer_courses:
        students_in_course = StudentProfile.objects.filter(course=course)
        for student in students_in_course:
            total_videos = RecordedVideo.objects.filter(course=course).count()
            completed_videos = VideoCompletion.objects.filter(student=student.user, video__course=course, is_completed=True).count()
            progress_percentage = (completed_videos / total_videos) * 100 if total_videos > 0 else 0
            student_progress_list.append({
                'student': student.user,
                'course': course,
                'progress_percentage': progress_percentage
            })
    context = {
        'student_progress_list': student_progress_list,
        'trainer': trainer
    }
    return render(request, 'studentprogress.html', context)










def Trainer_logout(request):
    logout(request)  # Log the user out
    return redirect('login')

