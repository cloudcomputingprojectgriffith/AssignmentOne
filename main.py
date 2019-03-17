import datetime
import os
import webapp2
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime

from myuser import MyUser
from gpu_data_model import Gpu_Data_Model
from gpu_details import Gpu_Details
from gpu_details_update import Gpu_details_update
from search_gpu import Search_gpu
import logging
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
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

        Gpu_details = Gpu_Data_Model.query().fetch(keys_only = True)
        if Gpu_details:
            template_values = {
                'logout_url': users.create_logout_url(self.request.uri),
                'gpu_db': Gpu_details,
            }
        else:
            template_values = {
                'logout_url' : users.create_logout_url(self.request.uri),
            }
        template = JINJA_ENVIRONMENT.get_template('mainpage.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        if action == 'Add Gpu Details':

            Name = self.request.get('Name')
            Manufacturer = self.request.get('Manufacturer')
            Date_Issued = datetime.strptime(self.request.get('Date_Issued'), '%Y-%m-%d')
            Geometry_Shader = self.request.get('Geometry_Shader')=='on'
            Tesselation_Shader = self.request.get('Tesselation_Shader')=='on'
            ShaderInt16 = self.request.get('ShaderInt16')=='on'
            Sparse_Binding = self.request.get('Sparse_Binding')=='on'
            Texture_Compression_ETC2 = self.request.get('Texture_Compression_ETC2')=='on'
            Vertex_Pipeline_Stores_And_Atomics = self.request.get('Vertex_Pipeline_Stores_And_Atomics')=='on'

            user = users.get_current_user()
            gpu_key = ndb.Key('Gpu_Data_Model', Name)
            gpu = gpu_key.get()
            if gpu is None:
                new_gpu = Gpu_Data_Model(id=Name, Name=Name, Manufacturer=Manufacturer, Date_Issued=Date_Issued,
                                             Geometry_Shader=Geometry_Shader, Tesselation_Shader=Tesselation_Shader,
                                             ShaderInt16=ShaderInt16, Sparse_Binding=Sparse_Binding,
                                             Texture_Compression_ETC2=Texture_Compression_ETC2,
                                             Vertex_Pipeline_Stores_And_Atomics=Vertex_Pipeline_Stores_And_Atomics)
                new_gpu.put()

                self.redirect('/')

            else:
                Gpu_details = Gpu_Data_Model.query().fetch(keys_only=True)
                template_values={
                    'error': 'Name already exists',
                    'gpu_db': Gpu_details,
                }
                template = JINJA_ENVIRONMENT.get_template('mainpage.html')
                self.response.write(template.render(template_values))

        elif action =="compareGPU":
            self.response.headers['Content-Type'] = 'text/html'
            user = users.get_current_user()
            if user == None:
                template_values = {
                    'login_url': users.create_login_url(self.request.uri)
                }
                template = JINJA_ENVIRONMENT.get_template('mainpage_guest.html')
                self.response.write(template.render(template_values))
                return

            compare_query = {}

            gpu_name = self.request.get_all('compare')
            #logger = logging.getLogger('scope.name')
            #logger.info(gpu_name)
            #logger.info("for:")
            for i in range(len(gpu_name)):
                compare_query[i] = Gpu_Data_Model.query()
                compare_query[i] = compare_query[i].filter(Gpu_Data_Model.Name == gpu_name[i])
                #logger.info(compare_query)
            #logger.info('end for')
            if (len(compare_query)) == 2:


                #logger.info(compare_query)
                template_values = {
                    'logout_url': users.create_logout_url(self.request.uri),
                    'compare_info': compare_query,
                    'value': len(gpu_name)
                    # 'logout_url': users.create_logout_url(self.request.uri),
                }

                template = JINJA_ENVIRONMENT.get_template('compare_gpu.html')

                self.response.write(template.render(template_values))

            else:
                Gpu_details = Gpu_Data_Model.query().fetch(keys_only=True)
                template_values = {
                    'logout_url': users.create_logout_url(self.request.uri),
                        'compareError': 'Invalid Selection!',
                    'gpu_db': Gpu_details,
                }
                template = JINJA_ENVIRONMENT.get_template('mainpage.html')
                self.response.write(template.render(template_values))



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/gpu_details', Gpu_Details),
    ('/gpu_details_update', Gpu_details_update),
    ('/search_gpu', Search_gpu)
])
