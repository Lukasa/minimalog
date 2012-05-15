from django.contrib.syndication.views import Feed
from posts.models import Post
from helpers import get_post_url, post_as_components
from blog.settings import BLOG_FULL_TITLE, BLOG_DESCRIPTION
import markdown

class LatestEntries(Feed):
    title = BLOG_FULL_TITLE
    link = '/'
    description = BLOG_DESCRIPTION

    def items(self):
        return Post.objects.order_by("-publication_date")[:10]

    def item_title(self, item):
        return post_as_components(item.body)[0]
    
    def item_description(self, item):
        first_para =  post_as_components(item.body)[1]
        return markdown.markdown(first_para)

    def item_link(self, item):
        return get_post_url(item)
