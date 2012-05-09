from django.db import models

class Post(models.Model):
    body = models.TextField()
    title = models.CharField(max_length=50)
    display_title = models.CharField(max_length=50)
    publication_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return self.author + u"'s comment on " + self.post.__unicode__()

