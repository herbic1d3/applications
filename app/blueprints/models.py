from django.db import models

from keys.models import Key


class Blueprint(models.Model):
    title = models.CharField(max_length=100)
    key = models.ForeignKey(Key, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
