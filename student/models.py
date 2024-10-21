from django.db import models
from django.contrib.auth.models import User
from adminapp.models import Trainer
from trainer.models import RecordedVideo

class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, default='Default Name')
    email = models.EmailField(max_length=100, default='default@example.com')
    phone = models.CharField(max_length=15)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending'
    )
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True)
    trainer_name = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        unique_together = ('trainer', 'course')

    def __str__(self):
        return f"{self.user.username}'s Profile"
    

class VideoRating(models.Model):
    video = models.ForeignKey(RecordedVideo, related_name='ratings', on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

class VideoCompletion(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(RecordedVideo, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

class Feedback(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class TrainerRating(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE) 
    rating = models.PositiveIntegerField()
