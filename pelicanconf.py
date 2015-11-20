#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'solarsail'
SITENAME = u'PlanetMeow'
SITEURL = ''

PATH = 'content'
STATIC_PATHS = ['blog', 'image', 'page']
ARTICLE_PATHS = ['blog']

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['cjk-auto-spacing', 'render_math']

THEME = "pelican-themes/pelican-bootstrap3"

TIMEZONE = 'Asia/Shanghai'
DEFAULT_DATE = 'fs'

DEFAULT_LANG = u'zh'

#FORMATTED_FIELDS = ['title']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

CJK_AUTO_SPACING_TITLE = True
#DIRECT_TEMPLATES = (('search',))
