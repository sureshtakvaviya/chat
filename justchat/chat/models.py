from django.contrib.auth.models import User
from django.db import models

class  Chat(models.Model):
    roomname=models.CharField(max_length=50)
    author = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

#     # def last_30_messages(self):
#     #     return Message.objects.order_by('-timestamp').all()[:30]


