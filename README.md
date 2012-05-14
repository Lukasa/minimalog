# Minimalog: Minimal blogging.

There are a million and one ways to start a blog. You can get a Wordpress
blog, or a Blogger blog, or download one of the millions of blogging
frameworks for Ruby on Rails or Django. Any of these methods will give you a
lovely blog, with many stunning features and shiny GUIs and stuff. Minimalog
does not have those things.

Do you want a nice web-based UI for writing your posts, with WYSIWYG editing?
Minimalog doesn't have that.

Do you want nice comment filtering so you don't have to worry about spam?
Minimalog doesn't have that either.

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

## Advantages

* __Secure__. There are no logins or login options available for either
administrators or commenters, so there is nothing to be abused. No input from
commenters is trusted, and the ORM should limit the exposure to SQL injection.

* __Anonymous__. As noted above, Minimalog does not provide accounts for
posters, administrators or commenters. Additionally, no analytics are provided
in the default configuration. Minimalog does not keep track of anyone.

* __Lightweight__. Because of its limited functionality, Minimalog is small.
Aside from translating posts out of Markdown format, Minimalog does almost
nothing.

* __Fast(-ish)__. The default install of Minimalog does not use Javascript or
much in the way of complex backend logic, and expects static files to be
hosted separately (e.g. in AWS). This should keep the blog fast.

## I'm sold. How do I use it?

To come.

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

