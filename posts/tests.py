# coding=utf-8
from django.test import TestCase
from posts.helpers import get_post_url, post_as_components, blogcontext
from posts.models import Post, Comment
from django.core.urlresolvers import reverse

class PostViewsTestCase(TestCase):
    fixtures = ['posts_test_data.json']

    def test_home_page_exists(self):
        response = self.client.get(reverse('blog_home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_templates(self):
        response = self.client.get(reverse('blog_home'))
        self.assertEqual([temp.name for temp in response.templates],
                         ['home.html', 'base.html'])

    def test_home_page_contains_recent_posts(self):
        response = self.client.get(reverse('blog_home'))
        self.assertEqual(len(response.context['posts']), 3)

    def test_home_page_has_titles(self):
        response = self.client.get(reverse('blog_home'))
        self.assertEqual([post[0] for post in response.context['posts']],
                         ['Building a Blog Part 3',
                          'Building a Blog Part 2',
                          'Building a Blog Part 1'])

    def test_home_page_has_paragraph_associated_with_each_title(self):
        response = self.client.get(reverse('blog_home'))

        paragraph_lengths=[len(post[1]) for post in response.context['posts']]

        for length in paragraph_lengths:
            self.assertTrue(length > 0)

    def test_home_page_each_paragraph_is_exactly_one_paragraph(self):
        response = self.client.get(reverse('blog_home'))

        paragraphs = [post[1] for post in response.context['posts']]

        for paragraph in paragraphs:
            sub_paras = paragraph.split('\n\n')
            self.assertEqual(len(sub_paras), 1)

    def test_archive_exists(self):
        response = self.client.get(reverse('blog_archive'))
        self.assertEqual(response.status_code, 200)

    def test_archive_uses_correct_templates(self):
        response = self.client.get(reverse('blog_archive'))
        self.assertEqual([temp.name for temp in response.templates],
                         ['archive.html', 'base.html'])

    def test_archive_contails_all_posts(self):
        response = self.client.get(reverse('blog_archive'))
        self.assertEqual(len(response.context['posts']), 3)

    def test_archive_has_titles(self):
        response = self.client.get(reverse('blog_archive'))
        self.assertEqual([post[0] for post in response.context['posts']],
                         ['Building a Blog Part 3',
                          'Building a Blog Part 2',
                          'Building a Blog Part 1'])

    def test_about_page_exists(self):
        response = self.client.get(reverse('blog_about_me'))
        self.assertEqual(response.status_code, 200)

    def test_about_page_uses_correct_templates(self):
        response = self.client.get(reverse('blog_about_me'))
        self.assertEqual([temp.name for temp in response.templates],
                         ['about.html', 'base.html'])

    def test_post_page_exists_for_post_in_db(self):
        response = self.client.get(
                           reverse('blog_post',
                           kwargs={'post_year': '2012',
                                   'post_month': '05',
                                   'post_title': '3_Building_A_Blog_Part_3'}
                                   ))
        self.assertEqual(response.status_code, 200)

    def test_post_page_does_not_exist_for_invalid_post(self):
        response = self.client.get(
                           reverse('blog_post',
                           kwargs={'post_year': '2012',
                                   'post_month': '05',
                                   'post_title': '4_Not_A_Post'}
                                  ))
        self.assertEqual(response.status_code, 404)

    def test_post_page_uses_correct_templates(self):
        response = self.client.get(
                           reverse('blog_post',
                           kwargs={'post_year': '2012',
                                   'post_month': '05',
                                   'post_title': '3_Building_A_Blog_Part_3'}
                                   ))
        self.assertEqual([temp.name for temp in response.templates],
                         ['post.html', 'base.html'])

    def test_post_page_context(self):
        response = self.client.get(
                           reverse('blog_post',
                           kwargs={'post_year': '2012',
                                   'post_month': '05',
                                   'post_title': '3_Building_A_Blog_Part_3'}
                                   ))
        self.assertEqual(response.context['post_title'],
                         'Building a Blog Part 3')
        self.assertTrue(len(response.context['post_body']) > 0)
        self.assertTrue(len(response.context['post_url']) > 0)
        self.assertTrue(response.context['comments_enabled'])
        self.assertEqual(len(response.context['comments']), 1)

    def test_post_page_handles_disabled_comments(self):
        response = self.client.get(
                           reverse('blog_post',
                           kwargs={'post_year': '2012',
                                   'post_month': '05',
                                   'post_title': '2_Building_A_Blog_Part_2'}
                                   ))
        self.assertEqual(response.context['comments_enabled'], False)
        self.assertEqual(len(response.context['comments']), 0)

    def test_post_comment_handles_valid_data(self):
        post = Post.objects.get(pk = 3)
        comments = Comment.objects.filter(post = post)
        self.assertEqual(len(comments), 1)

        response = self.client.post(
                           reverse('blog_post',
                           kwargs={'post_year': '2012',
                                   'post_month': '05',
                                   'post_title': '3_Building_A_Blog_Part_3'}
                                   ),
                                   {'name': 'Fred',
                                    'text': 'This is a comment.'}
                                   )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'],
                           'http://testserver' +
                           reverse('blog_post',
                           kwargs={'post_year': '2012',
                                   'post_month': '05',
                                   'post_title': '3_Building_A_Blog_Part_3'}
                                   ))

        comments = Comment.objects.filter(post = post)
        self.assertEqual(len(comments), 2)
        self.assertEqual(comments[1].author, 'Fred')
        self.assertEqual(comments[1].text, 'This is a comment.')

    def test_post_comment_handles_invalid_data(self):
        # 404 if we post to a nonexistent post.
        response = self.client.post(
                           reverse('blog_post',
                           kwargs={'post_year': '2012',
                                   'post_month': '05',
                                   'post_title': '4_Not_A_Post'}
                                  ))
        self.assertEqual(response.status_code, 404)

        # Confirm that we have the right number of comments.
        post = Post.objects.get(pk = 3)
        comments = Comment.objects.filter(post = post)
        self.assertEqual(len(comments), 1)

        # Try not sending data.
        response = self.client.post(
                           reverse('blog_post',
                           kwargs={'post_year': '2012',
                                   'post_month': '05',
                                   'post_title': '3_Building_A_Blog_Part_3'}
                                   ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors,
                         {'name': [u'This field is required.'],
                          'text': [u'This field is required.']})
        comments = Comment.objects.filter(post = post)
        self.assertEqual(len(comments), 1)

        # Try junk data.
        response = self.client.post(
                           reverse('blog_post',
                           kwargs={'post_year': '2012',
                                   'post_month': '05',
                                   'post_title': '3_Building_A_Blog_Part_3'}
                                   ),
                                   {'foo': 'bar', 'greasy': 'spoon'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors,
                         {'name': [u'This field is required.'],
                          'text': [u'This field is required.']})
        comments = Comment.objects.filter(post = post)
        self.assertEqual(len(comments), 1)

    def test_post_comment_handles_unicode_properly(self):
        post = Post.objects.get(pk = 3)
        comments = Comment.objects.filter(post = post)
        self.assertEqual(len(comments), 1)
        name = u'ᄏ℗♩ヶ菱'
        text = name

        response = self.client.post(
                           reverse('blog_post',
                           kwargs={'post_year': '2012',
                                   'post_month': '05',
                                   'post_title': '3_Building_A_Blog_Part_3'}
                                   ),
                                   {'name': name, 'text': text})
        self.assertEqual(response.status_code, 302)

        comments = Comment.objects.filter(post = post)
        self.assertEqual(comments[1].author, u'ᄏ℗♩ヶ菱')
        self.assertEqual(comments[1].text, u'ᄏ℗♩ヶ菱')

class HelpersTestCase(TestCase):
    fixtures = ['posts_test_data.json']

    def test_url_creation(self):
        test_post = Post.objects.all()[1]
        self.assertEqual(get_post_url(test_post),
                             reverse('blog_post',
                             kwargs={'post_year': '2012',
                                     'post_month': '05',
                                     'post_title': '2_Building_A_Blog_Part_2'}
                                     ))

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

    def test_blogcontext_returns_dict(self):
        output = blogcontext(object())

        self.assertTrue(isinstance(output, dict))

    def test_blogcontext_supplies_expected_variables(self):
        output = blogcontext(object())

        self.assertTrue(output['PAGE_AUTHOR'])
        self.assertTrue(output['BLOG_SHORT_TITLE'])
        self.assertTrue(output['BLOG_FULL_TITLE'])
        self.assertTrue(output['BLOG_ATTRIBUTION'])
        self.assertEqual(len(output), 9)

