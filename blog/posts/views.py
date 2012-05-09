from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from posts.models import Post, Comment
from django.http import Http404, HttpResponse

def post(request, post_title):
    # Try to find the post that corresponds to the title.
    try:
        found_post = Post.objects.get(title = post_title)
    except Post.DoesNotExist:
        raise Http404

    # Get the information in the form we want. This should be considered
    # subject to change.
    post_content = found_post.body.split('\n\n')
    post_title = post_content[0].strip('# ')
    post_remainder = u'\n\n'.join(post_content[1:])
    post_url = u'/blog/' + found_post.title + u'/'
    title = u'Lukasa | ' + post_title

    # Get all the comments associated with the post.
    comments = Comment.objects.filter(post = found_post).order_by("date")

    # Got to build up the relevant contexts.
    context = RequestContext(request,
            {'PAGE_TITLE': title,
             'PAGE_DESCRIPTION': None,
             'PAGE_AUTHOR': u'Cory Benfield',
             'post_title': post_title,
             'post_body': post_remainder,
             'post_url': post_url,
             'comments': comments})

    t = loader.get_template('post.html')

    return HttpResponse(t.render(context))

def home(request):
    # Here we want to show the most recent posts.
    posts = Post.objects.all().order_by("publication_date")[:5]
    data_for_output = []

    title = u"Lukasa's BLOGTIEM"

    # We don't want all of the blog post, just the title and first paragraph.
    # TODO: Should this be more resilient?
    for post in posts:
        content = post.body.split('\n\n')
        title = content[0].strip('# ')
        url = u'/blog/' + post.title + u'/'
        data_for_output.append( (title, content[1], url) )

    # Build up the context again.
    context = RequestContext(request,
              {'PAGE_TITLE': title,
               'PAGE_DESCRIPTION': u'A blog of technology, programming and life.',
               'PAGE_AUTHOR': u'Cory Benfield',
               'posts': data_for_output})

    t = loader.get_template('home.html')

    return HttpResponse(t.render(context))

def archive(request):
    # Here we want to show all of the post titles, sorted by date.
    posts = Post.objects.all().order_by("publication_date")
    data_for_output = []

    title = u"Lukasa | Archive"

    # Here we only need the titles and the urls.
    for post in posts:
        content = post.body.split('\n\n')
        title = content[0].strip('# ')
        url = u'/blog/' + post.title + u'/'
        data_for_output.append( (title, url) )

    context = RequestContext(request,
              {'PAGE_TITLE': title,
               'PAGE_DESCRIPTION': u'A list of blog posts.',
               'PAGE_AUTHOR': u'Cory Benfield',
               'posts': data_for_output})
    t = loader.get_template('archive.html')

    return HttpResponse(t.render(context))

