from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)

    def __unicode__(self):
        return self.name

class Post(models.Model):
    body = models.TextField()
    title = models.CharField(max_length=50)
    display_title = models.CharField(max_length=50)
    author = models.ForeignKey(Author)
    publication_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

