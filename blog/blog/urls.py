from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('posts.views',
    # Examples:
    url(r'^$', 'home', name='blog_home'),
    url(r'^(?P<post_year>\d{4})/(?P<post_month>\d{2})/(?P<post_title>\w+)/$',
        'post',
        name='blog_post'),
    url(r'^archive/$', 'archive', name='blog_archive'),
    url(r'^about/$', 'about', name='blog_about_me'),
    # url(r'^blog/', include('blog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
