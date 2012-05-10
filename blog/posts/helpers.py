from models import Post

def get_post_url(post):
    post_year = str(post.publication_date.year)
    post_month = '%02d' % post.publication_date.month
    post_title = post.title
    url = u'/blog/' + post_year + '/' + post_month + '/' + post_title + '/'
    return url
