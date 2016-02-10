#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'solarsail'
SITENAME = u'PlanetMeow'
SITEURL = ''

PATH = 'content'
STATIC_PATHS = ['image', 'page', 'extra/favicon.ico']
ARTICLE_PATHS = ['blog']

EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['cjk-auto-spacing', 'render_math', 'tag_cloud']

THEME = "pelican-themes/pelican-bootstrap3"
BOOTSTRAP_THEME = 'cosmo'

TIMEZONE = 'Asia/Shanghai'
DEFAULT_DATE = 'fs'

DEFAULT_LANG = u'zh'

#FORMATTED_FIELDS = ['title']

ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DISPLAY_TAGS_INLINE = True
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
TAGS_URL = 'tags.html'
DIRECT_TEMPLATES = ['index', 'categories', 'authors', 'archives', 'search']

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'))

# Social widget
SOCIAL = ()

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

CJK_AUTO_SPACING_TITLE = True
