from django.db import models

class Recipe (models.Model):
    title = models.CharField(max_length=255)
    recipe = models.CharField(max_length=5000)
    category = models.CharField(max_length=100)
    flavor_profiles = models.JSONField(default=list, help_text='A list containing the flavor profiler og the meal')

    def __str__(self):
        return self.title