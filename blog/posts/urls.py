from django.conf.urls import patterns, include, url

urlpatterns = patterns('posts.views',
    url(r'^$', 'home', name='blog_home'),
    url(r'^(?P<post_year>\d{4})/(?P<post_month>\d{2})/(?P<post_title>\w+)/$',
        'post',
        name='blog_post'),
    url(r'^archive/$', 'archive', name='blog_archive'),
    url(r'^about/$', 'about', name='blog_about_me'),
)
