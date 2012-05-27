# Minimalog: Minimal blogging.

There are a million and one ways to start a blog. You can get a Wordpress
blog, or a Blogger blog, or download one of the millions of blogging
frameworks for Ruby on Rails or Django. Any of these methods will give you a
lovely blog, with many stunning features and shiny GUIs and stuff. Minimalog
does not have those things.

Do you want a nice web-based UI for writing your posts, with WYSIWYG editing?
Minimalog doesn't have that.

Do you want to have multiple users contribute to your blog separately, without
requiring full-blown admin access? Minimalog doesn't do that.

Do you want it to play the bassoon? Minimalog doesn't do that, but to be fair
I don't think Wordpress does either. Certainly not without a plugin.

## So why should I bother?

Minimalog exists for people who have enough tech savvy that they want a blog
they can host themselves that does exactly one thing, blogging, not very well.
It is intended to be a lightweight blog framework which is fast (ish) and
secure (ish).

The basic configuration can be downloaded from Github and uploaded to Heroku
with minimal effort. Such a configuration uses no Javascript, has no off-site
links and generally doesn't do anything but allow you to post blog posts.

It should be possible to integrate this easily into an existing Django app: I
think I've moved as much information as possible into the app itself. If you
try and find that you need to make other changes to integrate Minimalog, I
welcome Pull Requests.

## How do I use Minimalog?

If you aren't familiar with the command-line, you should probably look
elsewhere for your blogging framework. Minimalog expects you to provide blog
posts to it in Markdown format, and provides a script for adding posts hosted
off-site (e.g. on GitHub) into the blog proper. This script will need to be
called from the command line (or the Heroku toolbelt), and you will be
expected to be comfortable with editing plain text files for config.

## What resources does Minimalog use?

Minimalog expects you to host static files on
[Amazon S3](http://aws.amazon.com/s3/). The comments functionality is provided
by [Disqus](http://disqus.com/). You **will need** accounts for both services
to use Minimalog.

## Advantages

* __Secure__. There are no logins or login options available for
administrators, so there is nothing to be abused.

* __Anonymous__. As noted above, Minimalog does not provide accounts for
posters or administrators. Additionally, no analytics are provided
in the default configuration. Minimalog does not keep track of anyone. S3 and
Disqus, however, may.

* __Lightweight__. Because of its limited functionality, Minimalog is small.
Aside from translating posts out of Markdown format, Minimalog does almost
nothing.

* __Fast(-ish)__. The default install of Minimalog does not use Javascript or
much in the way of complex backend logic, and expects static files to be
hosted separately (e.g. in AWS). This should keep the blog fast.

## I'm sold. How do I use it?

It's not all that hard. To get hold of the software, clone this repository.
Then, make sure you have all the packages installed, by running:
`pip install -r requirements.txt`.
Next, make sure you have an Amazon S3 account, and an empty S3 bucket.
Then, you need to make the following changes. First, replace the `about.html`
template with something that suits you better. Then, create a file called
`personal_settings.py` in the same directory as the already-existing
`settings.py` file. In this file, define some constants.

First, define the ones that are traditionally in the Django `settings.py`
file:

* __DEBUG__. `False` if you are in production, `True` for testing.
* __TEMPLATE\_DEBUG__. I set this equal to __DEBUG__.
* __DATABASES__. This depends on what database you're using. To see the
  correct format, look at the Django docs.
* __STATIC\_URL__. The URL to the S3 bucket you're storing your static
  files.
* __AWS\_STORAGE\_BUCKET\_NAME__. The name of the S3 bucket you're storing
  your static files in.
* __SECRET\_KEY__. This should be a random string used as a seed for the
  Django random number generator.

Next, define the compulsory ones for Minimalog:

* __BLOG\_AUTHOR__. The name of the person authoring the blog.
* __BLOG\_FULL\_TITLE__. The full-length title of the blog, e.g. 'My
  superawesome blog!'
* __BLOG\_SHORT\_TITLE__. A short-form version of the blog title, e.g
  'Superblog'.
* __BLOG\_PRE\_TITLE__. A string that will be placed before the titles of
  some of the pages, e.g. 'Superblog | '.
* __BLOG\_ATTRIBUTION__. The string you want to use as the attribution, e.g.
  'Created by Barney the Purple Dinosaur, 2052.'
* __BLOG\_DESCRIPTION__. A short string describing your blog for Google.

Next, provide the information you need in order to use Disqus:

* __DISQUS\_SHORTNAME__. The shortname of your Disqus forum. If you need help
  finding this information, see [here](http://docs.disqus.com/help/68/).

In the same file, you may define any of the following. They will be
automatically added to your sidebar.

* __GITHUB\_LINK__. A link to your GitHub page.
* __CODERWALL\_LINK__. A link to your Coderwall.
* __GPLUS\_LINK__. A link to your Google+ Profile.
* __LINKEDIN\_LINK__. A link to your LinkedIn profile.
* __TWITTER\_LINK__. A link to your Twitter profile.

Finally, define two environment variables in your shell:

* __S3\_KEY__. Your Amazon S3 key.
* __S3\_SECRET\_KEY__. Your Amazon S3 secret key.

With those defined, you should be ready to go! Make sure that all of the tests
run, by running `python manage.py test posts`, and ensuring they pass.

Then, upload all the static files you need to your S3 bucket, by running
`python manage.py collectstatic`. With that done, you should be ready to go!

## Uh, how do I get my blog posts into the database?

Depends. If you have access to the Django shell, you can import the Post model
and add them by hand. If not, I have provided a Django command that takes the
URL of a raw Markdown document and adds it to the DB. To run it, run:
`python manage.py addpost <post_url>`.

As an example, you can store your blog posts on Github. If you do so, and you
want to add them to the DB, you __must__ use the link to the __raw__ version
of the file.

## What about the license?

Minimalog is licensed under the MIT license. This gives you a wide range of
rights. I think it'd be polite if you acknowledged me if you use Minimalog,
but my self-esteem isn't so low that you have to.

## Acknowledgements

This project uses the excellent [Skeleton](http://www.getskeleton.com/) CSS
framework as a base point for the included CSS: I'd like to thank
[Dave Gamache](http://davegamache.com/) and his collaborators for their hard
work.

I'd also like to thank all of the people who have worked on all of the modules
listed in `requirements.txt`, who are too numerous to be listed here.

