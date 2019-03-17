import os
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb

from gpu_data_model import Gpu_Data_Model
from myuser import MyUser



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Search_gpu(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()

        if user == None:
            template_values = {
                'login_url' : users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template('mainpage_guest.html')
            self.response.write(template.render(template_values))
            return

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        if myuser == None:
            myuser = MyUser(id=user.user_id())
            myuser.put()

        gpu_query = Gpu_Data_Model().query().fetch()

        template_values = {
            'logout_url' : users.create_logout_url(self.request.uri),
            'gpu_model' : gpu_query
        }
        template = JINJA_ENVIRONMENT.get_template('search_gpu.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action = self.request.get('button')
        if action == 'Search':
           Geometry_Shader = bool(self.request.get('Geometry_Shader'))
           Tesselation_Shader = bool(self.request.get('Tesselation_Shader'))
           ShaderInt16 = bool(self.request.get('ShaderInt16'))
           Sparse_Binding = bool(self.request.get('Sparse_Binding'))
           Texture_Compression_ETC2 = bool(self.request.get('Texture_Compression_ETC2'))
           Vertex_Pipeline_Stores_And_Atomics = bool(self.request.get('Vertex_Pipeline_Stores_And_Atomics'))


           gpu_list = Gpu_Data_Model.query()

           if Geometry_Shader:
               gpu_list= gpu_list.filter(Gpu_Data_Model.Geometry_Shader==True)

           if Tesselation_Shader:
                gpu_list=gpu_list.filter(Gpu_Data_Model.Tesselation_Shader==True)

           if ShaderInt16:
                gpu_list=gpu_list.filter(Gpu_Data_Model.ShaderInt16==True)

           if Sparse_Binding:
                gpu_list=gpu_list.filter(Gpu_Data_Model.Sparse_Binding==True)

           if Texture_Compression_ETC2:
                gpu_list=gpu_list.filter(Gpu_Data_Model.Texture_Compression_ETC2==True)

           if Vertex_Pipeline_Stores_And_Atomics:
                gpu_list=gpu_list.filter(Gpu_Data_Model.Vertex_Pipeline_Stores_And_Atomicss==True)

           for i in gpu_list:
                self.response.write(i.Name + '<br/>')
