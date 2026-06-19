from django.db import models
from django.contrib.auth.models import User

class journalEntry(models.Model):
    ''' MOOD_CHOICES = [
        ('happy', '😊 Happy'),
        ('neutral', '😐 Neutral'),
        ('sad', '😞 Sad'),
        ('angry','😤angry'),
    ]'''


    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    # mood=models.CharField(max_length=10,choices=MOOD_CHOICES,default='neutral')
        
    def __str__(self):
            return self.title

   
    
   