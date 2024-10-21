
from .models import *
from django.contrib.auth import authenticate, login
from django.http import JsonResponse,HttpResponseRedirect
import stripe
import random
from adminapp.models import Admin_Model,Trainer
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from .models import StudentProfile, Course
from django.urls import reverse
from django.contrib.auth import logout
from trainer.models import RecordedVideo

stripe.api_key = settings.STRIPE_SECRET_KEY

def Home(request):
    return render(request, 'home.html')

def StudentRegister(request):
    if request.GET.get('payment_status') == 'cancelled':
        messages.warning(request, 'Payment was canceled. Please try again.')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        state = request.POST.get('state')
        course_id = request.POST.get('course')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        try:
            course = Course.objects.get(id=course_id)
            fee = course.fee
        except Course.DoesNotExist:
            messages.error(request, 'Selected course does not exist.')
            return redirect('register')

        if password == cpassword:
            if User.objects.filter(username=name).exists():
                messages.info(request, 'Username already exists!')
                return redirect('register')

            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists!')
                return redirect('register')

            else:
                user = User.objects.create_user(
                    username=name,
                    email=email,
                    password=password
                )
                trainers = Trainer.objects.filter(courses=course)
                if not trainers.exists():
                    messages.error(request, 'No trainers are available for the selected course.')
                    return redirect('register')
                assigned_trainer = random.choice(trainers)
                existing_profile = StudentProfile.objects.filter(trainer=assigned_trainer, course=course).first()
                if existing_profile:
                    messages.error(request, f'The trainer {assigned_trainer.user.username} is already assigned to another student for this course. Please wait.')
                    return redirect('register')
                student_profile = StudentProfile(
                    user=user,
                    name=name,
                    email=email,
                    phone=phone,
                    country=country,
                    state=state,
                    course=course,
                    fee=fee,
                    payment_status='Pending',
                    trainer=assigned_trainer,
                    trainer_name=assigned_trainer.user.username
                )
                student_profile.save()

                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'usd',
                                'product_data': {
                                    'name': course.name,
                                },
                                'unit_amount': int(fee * 100),
                            },
                            'quantity': 1,
                        },
                    ],
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('payment_success')) + '?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=request.build_absolute_uri(reverse('register')) + '?payment_status=cancelled',
                )

                return redirect(checkout_session.url)

        else:
            messages.info(request, 'Passwords do not match!')
            return redirect('register')

    else:
        courses = Course.objects.all()
        return render(request, 'studentregister.html', {'courses': courses})



def payment_success(request):
    session_id = request.GET.get('session_id')
    if session_id:
        try:
            checkout_session = stripe.checkout.Session.retrieve(session_id)
            if checkout_session.payment_status == 'paid':
                # Get the email from the checkout session (assumed to match user email)
                user_email = checkout_session.customer_details.email

                try:
                    user = User.objects.get(email=user_email)
                    student_profile = StudentProfile.objects.get(user=user)
                    # Update payment status
                    student_profile.payment_status = 'Completed'
                    student_profile.save()
                    messages.success(request, 'Payment successful! Your registration is complete.')
                except User.DoesNotExist:
                    messages.error(request, 'User not found. Please contact support.')
                except StudentProfile.DoesNotExist:
                    messages.error(request, 'Student profile not found. Please contact support.')
            else:
                messages.error(request, 'Payment could not be verified.')

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return redirect('login')

    
def get_course_fee(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        return JsonResponse({'fee': course.fee})
    except Course.DoesNotExist:
        return JsonResponse({'error': 'Course not found'}, status=404)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if Admin_Model.objects.filter(user=user).exists():
                login(request, user) 
                return redirect('admin_dashboard') 
            elif StudentProfile.objects.filter(user=user).exists():
                login(request, user)
                student_profile = StudentProfile.objects.get(user=user)
                course = student_profile.course
                video = RecordedVideo.objects.filter(course=course).first()

                if video:
                    return redirect('student_dashboard', video_id=video.id)
                else:
                    messages.error(request, 'No videos available for your course.')
                    return redirect('student_dashboard', video_id=0)
            elif Trainer.objects.filter(user=user).exists():
                login(request, user) 
                return redirect('trainer_dashboard')
            else:
                messages.error(request, 'Invalid user type')
                return redirect('login')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'login.html')



def student_profile(request):
    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        profile = None
    context = {
        'profile': profile,
        'username': request.user.username,
    }
    return render(request, 'profile.html', context)


def DashBoard(request,video_id=None):
    username = request.user.username
    student_profile = request.user.studentprofile
    course = student_profile.course 
    videos = RecordedVideo.objects.filter(course=course,)
    video = None
    if video_id:
        video = get_object_or_404(RecordedVideo, id=video_id, course=course)
    else:
        video = videos.first()

    return render(request, 'studentdash.html', {
        'username': username,
        'videos': videos,
        'video': video
    })

# def Trainer_details(request):
#     student_profile = StudentProfile.objects.get(user=request.user)
#     trainer = student_profile.trainer 
#     context = {
#         'student_profile': student_profile,
#         'trainer': trainer,
#     }
#     return render(request, 'trainerdetails.html', context)



def Trainer_details(request):
    trainer = Trainer.objects.first()
    has_rated = TrainerRating.objects.filter(trainer=trainer, student=request.user).exists()

    if request.method == 'POST':
        rating_value = int(request.POST.get('rating'))
        TrainerRating.objects.update_or_create(
            trainer=trainer,
            student=request.user,
            defaults={'rating': rating_value}
        )
        # Redirect back to the same page after rating submission
        return HttpResponseRedirect(request.path_info)

    context = {
        'trainer': trainer,
        'has_rated': has_rated,
        'rating': TrainerRating.objects.filter(trainer=trainer, student=request.user).first()
    }
    return render(request, 'trainerdetails.html', context)




def Uploaded_Videos(request):
    student_profile = request.user.studentprofile
    course = student_profile.course
    video_id = request.GET.get('video_id')
    if video_id:
        current_video = get_object_or_404(RecordedVideo, id=video_id, course=course)
    else:
        current_video = RecordedVideo.objects.filter(course=course).order_by('id').first()
    if not current_video:
        return render(request, 'uploadedvideos.html')
    previous_video = RecordedVideo.objects.filter(course=course, id__lt=current_video.id).order_by('-id').first()
    next_video = RecordedVideo.objects.filter(course=course, id__gt=current_video.id).order_by('id').first()
    try:
        existing_rating = VideoRating.objects.get(video=current_video, student=request.user)
        current_rating = existing_rating.rating
    except VideoRating.DoesNotExist:
        current_rating = 0
    if request.method == 'POST':
        if request.POST.get('action') == 'next_video':
            VideoCompletion.objects.update_or_create(
                video=current_video, student=request.user, defaults={'is_completed': True}
            )
        rating = request.POST.get('rating')
        if rating:
            VideoRating.objects.update_or_create(
                video=current_video, student=request.user,
                defaults={'rating': rating}
            )
    context = {
        'current_video': current_video,
        'previous_video': previous_video,
        'next_video': next_video,
        'current_rating': current_rating,
    }

    return render(request, 'uploadedvideos.html', context)



def progress_view(request):
    total_videos = RecordedVideo.objects.count()
    completed_videos = VideoCompletion.objects.filter(student=request.user, is_completed=True).count()
    progress_percentage = (completed_videos / total_videos) * 100 if total_videos > 0 else 0
    context = {
        'progress_percentage': progress_percentage,
    }

    return render(request, 'progress.html', context)



def feedback_view(request):
    if request.method == 'POST':
        feedback_content = request.POST.get('content')
        if feedback_content:
            Feedback.objects.create(student=request.user, content=feedback_content)
            return redirect('student_dashboard')

    feedbacks = Feedback.objects.filter(student=request.user).order_by('-created_at')
    return render(request, 'feedback.html', {'feedbacks': feedbacks})


def student_logout(request):
    logout(request)
    return redirect('login')