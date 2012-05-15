from django.core.management.base import BaseCommand, CommandError
from posts.models import Post
import requests

class Command(BaseCommand):
    args = '<url_to_raw_file>'
    help ='Adds a post from a url that points to the raw file.'

    def handle(self, *args, **options):
        for url in args:
            try:
                post = requests.get(url)

                if post.status_code == requests.codes.ok:
                    # Assume that the name of the post is the filename. Works for GitHub.
                    filename = '.'.join(url.split('/')[-1].split('.')[:-1])
                    p = Post(body = post.text, title = filename)
                    p.save()
                    self.stdout.write("Successfully added new post with url: '%s'" % filename)
                else:
                    raise CommandError('URL not valid.')
            except (requests.RequestException, requests.Timeout, requests.ConnectionError) as e:
                raise CommandError("A connection error was encountered.")
