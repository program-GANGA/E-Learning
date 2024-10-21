from django.db import models


class RecordedVideo(models.Model):
    title = models.CharField(max_length=100)  # Title for each video
    video = models.FileField(upload_to='videos/')  # Store videos in the media/videos folder
    course = models.ForeignKey('student.Course', related_name='videos', on_delete=models.CASCADE)  # ForeignKey to relate to a course

    def __str__(self):
        return self.title
# Create your models here.
