from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)
    score = models.IntegerField(default=0)
    best_score = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=[('win', 'Win'), ('loss', 'Loss')])

    def __str__(self):
        return f'{self.user.username} - {self.timestamp} - Score: {self.score}'
