from google.appengine.ext import ndb


class Gpu_Data_Model(ndb.Model):

    Name = ndb.StringProperty()
    Manufacturer = ndb.StringProperty()
    Date_Issued = ndb.DateProperty()
    Geometry_Shader = ndb.BooleanProperty()
    Tesselation_Shader = ndb.BooleanProperty()
    ShaderInt16 = ndb.BooleanProperty()
    Sparse_Binding = ndb.BooleanProperty()
    Texture_Compression_ETC2 = ndb.BooleanProperty()
    Vertex_Pipeline_Stores_And_Atomics = ndb.BooleanProperty()