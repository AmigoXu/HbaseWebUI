from django.test import TestCase, Client
import sys
from views import *


# Create your tests here.
reload(sys)
sys.setdefaultencoding('utf8')

class ViewsTest(TestCase):
    def setUp(self):
        pass
        
    def test_put(self):
        c = Client()
        inp1 = {u'cols': [u''], u'tbl': [u'tblname'], u'conn': [u'conn_str'], u'rk': [u'rk_str']}
        
        response1 = c.post('/hbase/ajax_getData/',inp1)
        print response1


#         inp['input'] = response1.encode('utf8')
#         print inp
#         response = c.post('/hbase/ajax_put/',inp)
#         print response.content