import webapp2
import jinja2
import os

from google.appengine.ext import ndb


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Gpu_Details(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        id = self.request.get('id')

        gpu_key = ndb.Key('Gpu_Data_Model', id)
        gpu = gpu_key.get()

        template_values = {
        'gpu' : gpu
        }

        template = JINJA_ENVIRONMENT.get_template('gpu_details.html')
        self.response.write(template.render(template_values))


        if self.request.get('button') == 'Cancel':
            self.redirect('/')
