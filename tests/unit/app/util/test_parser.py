from app.util.parser import GmlToGeojsonFilter, JsonXmlParser, XmlToJsonFilterChain
from lxml import etree
import pytest


class TestJsonXmlParser:

    def test_all(self, parser):
        assert parser.all('/ns1:root') == [{
            'a': ['1', '2'],
            'b': '1'
        }]

        assert parser.all('/ns1:root/ns2:a') == ['1', '2']
        assert parser.all('/ns1:root/ns2:b') == ['1']

    def test_contains(self, parser):
        assert parser.contains('/ns1:root/ns2:a') is True
        assert parser.contains('/ns1:root/ns2:c') is False

    def test_first(self, parser):
        assert parser.first('/ns1:root/ns2:a') == '1'

    def test_last(self, parser):
        assert parser.last('/ns1:root/ns2:a') == '2'

    @pytest.fixture
    def parser(self, xml_tree) -> JsonXmlParser:
        return JsonXmlParser(xml_tree, namespaces=NAMESPACES)

    @pytest.fixture
    def xml_tree(self) -> etree.ElementTree:
        return etree.fromstring(TEST_XML)


class TestDefaultXmlToJsonFilter:

    def test_filter(self):
        chain = XmlToJsonFilterChain([])

        element = etree.fromstring(TEST_XML)
        output = chain(element)

        assert output == {
            'a': ['1', '2'],
            'b': '1'
        }


class TestGmlToGeojsonFilter:

    def test_filter_coordinates(self):
        chain = XmlToJsonFilterChain([GmlToGeojsonFilter(precision=2)])

        element = etree.fromstring(TEST_GML_COORDINATES)
        output = chain(element)

        assert output == {
            'type': 'Point',
            'coordinates': [45.34, -94.33]
        }

    def test_filter_pos(self):
        chain = XmlToJsonFilterChain([GmlToGeojsonFilter(precision=2)])

        element = etree.fromstring(TEST_GML_POS)
        output = chain(element)

        assert output == {
            'type': 'Point',
            'coordinates': [45.34, -94.33]
        }


NAMESPACES = {
    'gml': 'http://www.opengis.net/gml/3.2',
    'ns1': 'http://www.bogus.net/ns1',
    'ns2': 'http://www.bogus.net/ns2'
}


TEST_XML = '''
<ns1:root xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:ns1="http://www.bogus.net/ns1" xmlns:ns2="http://www.bogus.net/ns2">
  <ns2:a>1</ns2:a>
  <ns2:a>2</ns2:a>
  <ns2:b>1</ns2:b>
</ns1:root>
'''  # noqa: E501

TEST_GML_COORDINATES = \
    '<gml:coordinates xmlns:gml="http://www.opengis.net/gml/3.2">45.343239, -94.329753</gml:coordinates>'

TEST_GML_POS = '<gml:pos xmlns:gml="http://www.opengis.net/gml/3.2">45.343239 -94.329753</gml:pos>'
