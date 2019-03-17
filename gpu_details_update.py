import webapp2
import jinja2
import os

from google.appengine.ext import ndb
from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Gpu_details_update(webapp2.RequestHandler):
    Name = ""
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        global Name
        Name = self.request.get('Name')
        gpu_key = ndb.Key('Gpu_Data_Model', Name)
        gpu = gpu_key.get()

        template_values = {
        'gpu' : gpu
        }

        template = JINJA_ENVIRONMENT.get_template('gpu_details_update.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content - Type'] = 'text / html'
        action = self.request.get('button')
        if action == 'Update':

            gpu_key = ndb.Key('Gpu_Data_Model', Name)
            gpu_update = gpu_key.get()



            gpu_update.Manufacturer = self.request.get('Manufacturer')
            gpu_update.Date_Issued = datetime.strptime(self.request.get('Date_Issued'), '%Y-%m-%d')
            gpu_update.Geometry_Shader = bool(self.request.get('Geometry_Shader'))
            gpu_update.Tesselation_Shader = bool(self.request.get('Tesselation_Shader'))
            gpu_update.ShaderInt16 = bool(self.request.get('ShaderInt16'))
            gpu_update.Sparse_Binding = bool(self.request.get('Sparse_Binding'))
            gpu_update.Texture_Compression_ETC2 = bool(self.request.get('Texture_Compression_ETC2'))
            gpu_update.Vertex_Pipeline_Stores_And_Atomics = bool(self.request.get('Vertex_Pipeline_Stores_And_Atomics'))
            gpu_update.put()

            self.redirect('/gpu_details?id='+Name)

        elif self.request.get('button') == 'Cancel':
            self.redirect('/')
