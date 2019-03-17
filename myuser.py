from google.appengine.ext import ndb
from gpu_data_model import Gpu_Data_Model

class MyUser(ndb.Model):
    username = ndb.StringProperty()
    gpu_db = ndb.StructuredProperty(Gpu_Data_Model, repeated=True)