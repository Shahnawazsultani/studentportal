from django.db import models
from Profile.models import User
# Create your models here.

class Course(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    enrolledBy = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)
    enrolledDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
 
class Enrollment(models.Model):
    reference = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Invoice: {self.reference}, Course ID: {self.course_id}, User: {self.user.username}"
