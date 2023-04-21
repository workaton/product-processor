import os
from collections import OrderedDict
from datetime import datetime

# from nose.tools import raises, assert_equal
# from nose_parameterized import parameterized
import pytest

from app.spot.stq.stq import StqProductGenerator, StqProduct
from app.spot.stq.template import TemplateEngine


class TestStqProductGenerator:
    '''Test the generator for STQ products'''
        
    @pytest.fixture
    def generator(self):
        return StqProductGenerator(TemplateEngine('./app/spot/stq/templates'))

    def test_deleted(self,generator):
        '''Test STQ generation for deleted action'''

        filename = "products/deleted.stq"
        filepath =  os.path.join(os.path.dirname(__file__), filename)
        with open (filepath) as file:
            data = file.read().replace('\n', '\r\r\n')

        product = generator.render(TEST_DELETED)
        assert product.body == data
        assert product.id == 1500001
        assert product.update == 0
    
    def test_feedback(self,generator):
        '''Test STQ generation for feedback action'''

        filename = "products/feedback.stq"
        filepath =  os.path.join(os.path.dirname(__file__), filename)
        with open (filepath) as file:
            data = file.read().replace('\n', '\r\r\n')

        product = generator.render(TEST_FEEDBACK)
        assert product.body == data
        assert product.id == 1500001
        assert product.update == 0

    def test_full(self,generator):
        '''Test a fully specified STQ'''

        filename = "products/full.stq"
        filepath =  os.path.join(os.path.dirname(__file__), filename)
        with open (filepath) as file:
            data = file.read().replace('\n', '\r\r\n')

        product = generator.render(TEST_FULL)
        assert product.body == data
        assert product.id == 1500001
        assert product.update == 0

    def test_minimal(self,generator):
        '''Test an STQ with as little set as possible'''

        filename = "products/minimal.stq"
        filepath =  os.path.join(os.path.dirname(__file__), filename)
        with open (filepath) as file:
            data = file.read().replace('\n', '\r\r\n')
        
        product = generator.render(TEST_MINIMAL)
        assert product.body == data
        assert product.id == 1500001
        assert product.update == 0

    def test_modified(self,generator):
        '''Test STQ generation for modified action'''

        filename = "products/modified.stq"
        filepath =  os.path.join(os.path.dirname(__file__), filename)
        with open (filepath) as file:
            data = file.read().replace('\n', '\r\r\n')

        product = generator.render(TEST_MODIFIED)
        assert product.body == data
        assert product.id == 1500001
        assert product.update == 0
    

TEST_MINIMAL = {
    'now':           datetime(2015, 7, 27, 10, 30).strftime("%Y-%m-%d %H:%M:%S"),
    'action':        'immediate',
    'elements':      {},
    'formatting':    [],
    'observations':  [],
    'id':            1500001,
    'update':        0,
    'site':          'EAX',
    'station':       'KEAX',
    'timezone':      'CST',
    'start_time':    datetime(2015, 7, 27, 11, 30).strftime("%Y-%m-%d %H:%M:%S"),
    'deliver_time':  datetime(2015, 7, 28, 8, 0).strftime("%Y-%m-%d %H:%M:%S"),
    'submit_time':   datetime(2015, 7, 27, 11, 0).strftime("%Y-%m-%d %H:%M:%S"),
    'project_name':  'Minimal Test Results',
    'project_type':  'Wildfire',
    'reason':        'TEST',
    'agency':        None,
    'official':      None,
    'phone':         None,
    'phone_ext':     None,
    'email':         None,
    'fax':           None,
    'state':         'MO',
    'lat':           39.1189,
    'lon':           (-94.5207),
    'exposure':      None,
    'fuel_type':     None,
    'sheltering':    None,
    'min_elevation': None,
    'max_elevation': None,
    'size':          None,
    'hysplit':       0,
    'remarks':       None
}

TEST_DELETED = dict(TEST_MINIMAL)
TEST_DELETED.update(action='deleted')

TEST_FEEDBACK = dict(TEST_MINIMAL)
TEST_FEEDBACK.update(action='feedback')

TEST_MODIFIED = dict(TEST_MINIMAL)
TEST_MODIFIED.update(action='modified')

TEST_FULL = dict(TEST_MINIMAL)
TEST_FULL.update(
    action='observation',
    project_name='Example Test Results',
    agency='Testing Agency',
    official='Testing Official',
    phone='555-555-5555',
    phone_ext='5555',
    email='test@test.test',
    fax='444-444-4444',
    exposure='North',
    fuel_type='grass',
    sheltering='unsheltered',
    min_elevation=111,
    max_elevation=888,
    size=33,
    elements=OrderedDict([
        ('Chance of Wetting Rain', [0, 0, 0, 1]),
        ('Max/Min Temperature', [0, 0, 0, 1]),
        ('Sky/Weather', [0, 0, 0, 1]),
        ('Transport Winds', [0, 0, 0, 1]),
        ('Mixing Height', [0, 0, 0, 1]),
        ('Wind (20 FT)', [0, 0, 0, 1]),
        ('Haines Index', [0, 0, 0, 1]),
        ('Max/Min Humidity', [0, 0, 0, 1])
    ]),
    formatting=[
        {
            'period': 1,
            'type': 'C',
            'temporal_res': 1
        },
        {
            'period': 2,
            'type': 'C',
            'temporal_res': 1
        },
        {
            'period': 3,
            'type': 'C',
            'temporal_res': 1
        },
        {
            'period': 4,
            'type': 'C',
            'temporal_res': 1
        }
    ],
    observations=[
        {
            'source': 'Test source',
            'data': OrderedDict([
                ('WB', 11),
                ('Temp', 11),
                ('Sky', 'Clear'),
                ('Elev', 666),
                ('Rmks', 'TEST'),
                ('Td', 11),
                ('RH', 11),
                ('Wind', '11@N'),
                ('Wx', 'Rain')
            ]),
            'time': datetime(2015, 7, 27, 6, 0).strftime("%Y-%m-%d %H:%M:%S")
        }
    ],
    remarks='How much wood could a woodchuck chuck if a woodchuck could chuck '
    'wood?'
)

