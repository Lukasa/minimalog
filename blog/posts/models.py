from django.db import models

class Post(models.Model):
    body = models.TextField()
    title = models.CharField(max_length=50)
    display_title = models.CharField(max_length=50)
    publication_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

