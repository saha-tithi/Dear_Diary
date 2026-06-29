from django.db import models
from django.contrib.auth.models import User

class journalEntry(models.Model):
    MOOD_CHOICES = [
        ('happy', '😊 Happy'),
        ("calm", "😌 Calm"),
        ('neutral', '😐 Neutral'),
        ('sad', '😢 Sad'),
        ('angry','😤angry'),
        ("excited", "🤩 Excited"),
        ("tired", "😴 Tired"),
        ]


    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    content=models.TextField()
    gratitude=models.TextField(blank=True)
    tomorrow_goal = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    is_favorite=models.BooleanField(default=False)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    mood=models.CharField(max_length=20,choices=MOOD_CHOICES,default='neutral')
        
    def __str__(self):
            return self.title
    class Meta:
        ordering = ['-created_at']

   
    
   