from django.test import TestCase
from posts.helpers import get_post_url, post_as_components
from posts.models import Post

class PostViewsTestCase(TestCase):
    fixtures = ['posts_test_data.json']

    def test_home_page_exists(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_templates(self):
        response = self.client.get('/')
        self.assertEqual([temp.name for temp in response.templates],
                         ['home.html', 'base.html'])

    def test_home_page_contains_recent_posts(self):
        response = self.client.get('/')
        self.assertEqual(len(response.context['posts']), 3)

    def test_home_page_has_titles(self):
        response = self.client.get('/')
        self.assertEqual([post[0] for post in response.context['posts']],
                         ['Building a Blog Part 3',
                          'Building a Blog Part 2',
                          'Building a Blog Part 1'])

    def test_home_page_has_paragraph_associated_with_each_title(self):
        response = self.client.get('/')

        paragraph_lengths=[len(post[1]) for post in response.context['posts']]

        for length in paragraph_lengths:
            self.assertTrue(length > 0)

    def test_home_page_each_paragraph_is_exactly_one_paragraph(self):
        response = self.client.get('/')

        paragraphs = [post[1] for post in response.context['posts']]

        for paragraph in paragraphs:
            sub_paras = paragraph.split('\n\n')
            self.assertEqual(len(sub_paras), 1)

    def test_archive_exists(self):
        response = self.client.get('/archive/')
        self.assertEqual(response.status_code, 200)

    def test_archive_uses_correct_templates(self):
        response = self.client.get('/archive/')
        self.assertEqual([temp.name for temp in response.templates],
                         ['archive.html', 'base.html'])

    def test_archive_contails_all_posts(self):
        response = self.client.get('/archive/')
        self.assertEqual(len(response.context['posts']), 3)

    def test_archive_has_titles(self):
        response = self.client.get('/archive/')
        self.assertEqual([post[0] for post in response.context['posts']],
                         ['Building a Blog Part 3',
                          'Building a Blog Part 2',
                          'Building a Blog Part 1'])

    def test_about_page_exists(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_about_page_uses_correct_templates(self):
        response = self.client.get('/about/')
        self.assertEqual([temp.name for temp in response.templates],
                         ['about.html', 'base.html'])

    def test_post_page_exists_for_post_in_db(self):
        response = self.client.get('/blog/2012/05/3_Building_A_Blog_Part_3/')
        self.assertEqual(response.status_code, 200)

    def test_post_page_does_not_exist_for_invalid_post(self):
        response = self.client.get('/blog/2012/05/4_Not_A_Post/')
        self.assertEqual(response.status_code, 404)

    def test_post_page_uses_correct_templates(self):
        response = self.client.get('/blog/2012/05/3_Building_A_Blog_Part_3/')
        self.assertEqual([temp.name for temp in response.templates],
                         ['post.html', 'base.html'])

    def test_post_page_context(self):
        response = self.client.get('/blog/2012/05/3_Building_A_Blog_Part_3/')
        self.assertEqual(response.context['post_title'],
                         'Building a Blog Part 3')
        self.assertTrue(len(response.context['post_body']) > 0)
        self.assertTrue(len(response.context['post_url']) > 0)
        self.assertTrue(response.context['comments_enabled'])
        self.assertEqual(len(response.context['comments']), 1)

class HelpersTestCase(TestCase):
    fixtures = ['posts_test_data.json']

    def test_url_creation(self):
        test_post = Post.objects.all()[1]
        self.assertEqual(get_post_url(test_post),
                         '/blog/2012/05/2_Building_A_Blog_Part_2/')

    def test_url_creation_fails_if_non_post_is_passed(self):
        test_post = object()
        self.assertRaises(AttributeError, get_post_url, test_post)

    def test_post_splitting(self):
        post_text = '''### Post Title

This is the first paragraph.

This is the second paragraph.'''

        title, first_para, body = post_as_components(post_text)
        self.assertEqual(title, 'Post Title')
        self.assertEqual(first_para, 'This is the first paragraph.')
        self.assertEqual(body, 'This is the first paragraph.\n\n' +
                               'This is the second paragraph.')

