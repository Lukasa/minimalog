from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from posts.models import Post
from django.http import Http404, HttpResponse

def home(request):
    return render_to_response('home.html', context_instance=RequestContext(request))

def post(request, post_title):

    # Try to find the post that corresponds to the title.
    try:
        found_post = Post.objects.get(title = post_title)
    except Post.DoesNotExist:
        raise Http404

    title = u'Lukasa | ' + found_post.display_title

    # Got to build up the relevant contexts.
    context = RequestContext(request,
            {'PAGE_TITLE': title,
             'PAGE_DESCRIPTION': None,
             'PAGE_AUTHOR': found_post.author.name,
             'BODY': found_post.body})

    t = loader.get_template('post.html')

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

