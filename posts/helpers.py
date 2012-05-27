from models import Post
from django.core.urlresolvers import reverse
from blog.settings import ( BLOG_AUTHOR, BLOG_FULL_TITLE,
                            BLOG_SHORT_TITLE, BLOG_ATTRIBUTION,
                            DISQUS_SHORTNAME, GPLUS_LINK, LINKEDIN_LINK,
                            TWITTER_LINK, GITHUB_LINK, CODERWALL_LINK, DEBUG )

def get_post_url(post):
    post_year = str(post.publication_date.year)
    post_month = '%02d' % post.publication_date.month
    post_title = post.title
    #url = u'/blog/' + post_year + '/' + post_month + '/' + post_title + '/'
    url = reverse('blog_post', kwargs={'post_year': post_year,
                                       'post_month': post_month,
                                       'post_title': post_title})
    return url

def post_as_components(post_text):
    ''' This function returns the components of a blog post for use with other
    functions. Given a Markdown formatted post, it returns a three-tuple. The
    first element is the blog title (not markdowned), the second is the first
    paragraph (in Markdown format) and the third is the entire post body (in
    Markdown format).
    '''
    post_content = post_text.split('\n\n')
    title = post_content[0].strip('# ')
    first_para = post_content[1]
    body = u'\n\n'.join(post_content[1:])
    return (title, first_para, body)

def blogcontext(request):
    '''This function acts as a Django context processor that injects some of
    the globals we want into the templates. It takes a request, but does
    nothing with it.'''
    context_dict = {'PAGE_AUTHOR': BLOG_AUTHOR,
                    'BLOG_SHORT_TITLE': BLOG_SHORT_TITLE,
                    'BLOG_FULL_TITLE': BLOG_FULL_TITLE,
                    'BLOG_ATTRIBUTION': BLOG_ATTRIBUTION,
                    'DISQUS_SHORTNAME': DISQUS_SHORTNAME,
                    'DEBUG': DEBUG,
                    'GPLUS_LINK': GPLUS_LINK,
                    'LINKEDIN_LINK': LINKEDIN_LINK,
                    'TWITTER_LINK': TWITTER_LINK,
                    'GITHUB_LINK': GITHUB_LINK,
                    'CODERWALL_LINK': CODERWALL_LINK}
    return context_dict

