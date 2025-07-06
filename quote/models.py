from django.db import models

class Quote(models.Model):
    author_name = models.CharField(max_length=400, blank=True)
    category = models.CharField(max_length=400, default='Sad')
    quote = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author_name} - {self.quote[:20]}"