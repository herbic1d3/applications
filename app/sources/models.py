from django.db import models

from blueprints.models import Blueprint


class Source(models.Model):
    blueprint = models.ForeignKey(Blueprint, on_delete=models.CASCADE)
    source = models.URLField(max_length=200, blank=False)

    def __str__(self):
        return str(self.source)
