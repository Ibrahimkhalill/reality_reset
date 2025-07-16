from django.db import models
from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class TermsAndConditions(models.Model):
    content = RichTextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class DailyFeeling(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    intensity = models.IntegerField(choices=[(i, i) for i in range(1, 11)])  # 1 to 10
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.intensity}"






class DailyMood(models.Model):
    MOOD_CHOICES = [
        ('low', 'Low'),
        ('energized', 'Energized'),
        ('hopeful', 'Hopeful'),
        ('overwhelmed', 'Overwhelmed'),
        ('frustrated', 'Frustrated'),
        ('drained', 'Drained'),
        ('disconnected', 'Disconnected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mood} - {self.date}"