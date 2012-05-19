from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from posts.models import Post, Comment
from django.http import Http404, HttpResponse, HttpResponseRedirect
from forms import CommentForm
from helpers import get_post_url, post_as_components
from blog.settings import BLOG_PRE_TITLE, BLOG_FULL_TITLE, BLOG_DESCRIPTION

def post(request, post_year, post_month, post_title):
    # Try to find the post that corresponds to the title.
    possibilities = Post.objects.filter(
                        publication_date__year = post_year
                    ).filter(
                        publication_date__month = post_month
                    ).filter(
                        title = post_title
                    )

    if len(possibilities) == 1:
        found_post = possibilities[0]
    else:
        raise Http404

    # If this is hit by a POST, someone is making a comment.
    if request.method == 'POST':
        form = CommentForm(request.POST)

        # Check form validity. If not valid, we'll drop through and render the
        # page.
        if form.is_valid():
            # Hooray, form is filled out ok! Create a new comment.
            body_text = form.cleaned_data['text']
            comment_author = form.cleaned_data['name']

            comment = Comment(text   = body_text,
                              author = comment_author,
                              post   = found_post)
            comment.save()
            # At this point, we're happy to drop through and render the page.
            return HttpResponseRedirect(request.path)
    else:
        # Return an empty form and render the page.
        form = CommentForm()

    # Get the information in the form we want. This should be considered
    # subject to change.
    # Begin with the post title and body.
    post_components = post_as_components(found_post.body)
    post_title = post_components[0]
    post_remainder = post_components[2]

    # Other ancillary stuff.
    post_url = get_post_url(found_post)
    page_title = BLOG_PRE_TITLE + post_title
    comments_enabled = found_post.enable_comments

    # Get all the comments associated with the post. Only bother with this if
    # the comments are enabled on the post.
    if comments_enabled:
        comments = Comment.objects.filter(post = found_post).order_by("date")
    else:
        comments = []

    # Got to build up the relevant contexts.
    context = RequestContext(request,
            {'PAGE_TITLE': page_title,
             'PAGE_DESCRIPTION': None,
             'post_title': post_title,
             'post_body': post_remainder,
             'post_url': post_url,
             'comments_enabled': comments_enabled,
             'comments': comments,
             'publication_date': found_post.publication_date,
             'form': form})

    t = loader.get_template('post.html')

    return HttpResponse(t.render(context))

def home(request):
    # Here we want to show the most recent posts.
    posts = Post.objects.order_by("-publication_date")[:5]
    data_for_output = []

    post_title = BLOG_FULL_TITLE

    # We don't want all of the blog post, just the title and first paragraph.
    # TODO: Should this be more resilient?
    for post in posts:
        title, first_para, body = post_as_components(post.body)
        url = get_post_url(post)
        data_for_output.append( (title, first_para, url) )

    # Build up the context again.
    context = RequestContext(request,
              {'PAGE_TITLE': post_title,
               'PAGE_DESCRIPTION': BLOG_DESCRIPTION,
               'posts': data_for_output})

    t = loader.get_template('home.html')

    return HttpResponse(t.render(context))

def archive(request):
    # Here we want to show all of the post titles, sorted by date.
    posts = Post.objects.order_by("-publication_date").all()
    data_for_output = []

    page_title = BLOG_PRE_TITLE + u" Archive"

    # Here we only need the titles and the urls.
    for post in posts:
        title = post_as_components(post.body)[0]
        url = get_post_url(post)
        data_for_output.append( (title, url) )

    context = RequestContext(request,
              {'PAGE_TITLE': page_title,
               'PAGE_DESCRIPTION': u'A list of blog posts.',
               'posts': data_for_output})
    t = loader.get_template('archive.html')

    return HttpResponse(t.render(context))

def about(request):
    # Render the About Me page.

    page_title = BLOG_PRE_TITLE + u' About Me'
    page_description = u'A brief description of me.'

    context = RequestContext(request,
              {'PAGE_TITLE': page_title,
               'PAGE_DESCRIPTION': page_description})
    t = loader.get_template('about.html')

    return HttpResponse(t.render(context))

