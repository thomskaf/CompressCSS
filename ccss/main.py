#!/usr/bin/env python
import os
import re
import cgi
import jinja2
import random
import webapp2
from google.appengine.ext import ndb
from datetime import datetime, timedelta
from ccss import compress_css


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


class CSSFile(ndb.Model):
    file_name = ndb.IntegerProperty()
    css_code = ndb.TextProperty()
    datetime = ndb.DateTimeProperty(auto_now_add=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        css_file_name = random.randint(10000, 99999)
        template_values = {
            'css_file_name': css_file_name,
        }

        template = JINJA_ENVIRONMENT.get_template('template.html')
        self.response.write(template.render(template_values))


class CompressCSS(webapp2.RequestHandler):
    def post(self):
        compressed_css = compress_css(self.request.get('css'))
        db = CSSFile()
        db.file_name = int(cgi.escape(self.request.get('filename')))
        db.css_code = compressed_css
        db.put()
        self.response.write(compressed_css)

    def get(self, filename):
        file_name = int(self.request.url.split('/')[4])
        css = CSSFile.query(CSSFile.file_name == file_name)

        self.response.headers['Content-Disposition'] = 'attachment; filename=compressed.css'
        self.response.write('\n'.join(line.strip() for line in re.findall(r'.{1,700}(?:\s+|$)', css.get().css_code)))


class Tmpfiles(webapp2.RequestHandler):
    def get(self):
        query = CSSFile.query()
        items = query.fetch()

        for item in items:
            if datetime.now() - timedelta(minutes=30) > item.datetime:
                item.key.delete()


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/compress', CompressCSS),
    (r'/get/(\d+)', CompressCSS),
    ('/delete-tmp-files', Tmpfiles)
], debug=False)
