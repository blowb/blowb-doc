#!/usr/bin/python3

# Generate sitemap

from __future__ import print_function

import fnmatch
import os
import time

SITEURL = 'http://docs.blowb.org'
EXCLUDE_FILES = ['index_printing']

print('''
<?xml version="1.0" encoding="UTF-8"?>
<urlset
    xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
                        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
 <url>
''')

# search for all *.rst files, replace .rst with .html, and prepend the site base url.
for root, dirnames, filenames in os.walk('.'):
    for filename in fnmatch.filter(filenames, '*.rst'):
        excluded = False
        for ex in EXCLUDE_FILES:
            if ex + '.rst' == filename:
                excluded = True
                break

        if excluded:
            continue

        f = list(filename)
        f[-3:]= 'html'
        filename = "".join(f)
        path = os.path.normpath(os.path.join(root, filename))
        url = SITEURL + '/' + path
        print('''
        <url>
         <loc>{}</loc>
         <lastmod>{}</lastmod>
        </url>
        '''.format(url, time.strftime("%Y-%m-%d")))

print('</urlset>')
