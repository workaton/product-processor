from __future__ import annotations

from app.util.parser import GmlToGeojsonFilter
from lxml import etree
from ngitws.typing import JsonObject

from .base import XmlExtractor


class SigmetExtractor(XmlExtractor):
    """Metadata extractor for AIRMET/SIGMET XML products."""

    XML_NAMESPACES = {
        'aixm': 'http://www.aixm.aero/schema/5.1.1',
        'gml': 'http://www.opengis.net/gml/3.2',
        'iwxxm11': 'http://icao.int/iwxxm/1.1',
        'iwxxm21': 'http://icao.int/iwxxm/2.1',
        'iwxxm3': 'http://icao.int/iwxxm/3.0',
        'iwxxmus10': 'http://nws.weather.gov/schemas/IWXXM-US/1.0/Release',
        'saf': 'http://icao.int/saf/1.1',
        'uswx10': 'http://nws.weather.gov/schemas/USWX/1.0',
        'xlink': 'http://www.w3.org/1999/xlink'
    }

    def __init__(self):
        super().__init__(namespaces=self.XML_NAMESPACES)

    async def _extract(self, xml_tree: etree.ElementTree) -> JsonObject:
        parser = self.json_parser(xml_tree, filters=[GmlToGeojsonFilter([
            '{http://www.aixm.aero/schema/5.1.1}Surface'
        ])])
        if parser.contains('//iwxxm3:AIRMET'):
            evolving = '//iwxxm3:AIRMETEvolvingConditionCollection'
        elif parser.contains('//iwxxm3:SIGMET'):
            evolving = '//iwxxm3:SIGMETEvolvingConditionCollection'
        elif parser.contains('//iwxxm21:AIRMET'):
            evolving = '//iwxxm3:AIRMETEvolvingConditionCollection'
        elif parser.contains('//iwxxm21:SIGMET'):
            evolving = '//iwxxm3:SIGMETEvolvingConditionCollection'
        else:
            raise RuntimeError('XML document is not a recognized AIRMET or SIGMET product')

        issue_time = parser.first('//iwxxm21|iwxxm3:issueTime/gml:TimeInstant/gml:timePosition')
        issuing_unit = parser.first('//iwxxm3:issuingAirTrafficServicesUnit//aixm:designator')
        watch_office_id = parser.first('//iwxxm3:originatingMeteorologicalWatchOffice//aixm:designator')
        issuing_region = parser.first('//iwxxm3:issuingAirTrafficServicesRegion//aixm:designator')
        sequence_number = parser.first('//iwxxm3:sequenceNumber')
        phenomenon = parser.first('//iwxxm3:phenomenon/@xlink:href')
        valid_start = parser.first('//iwxxm3:validPeriod/gml:TimePeriod/gml:beginPosition')
        valid_end = parser.first('//iwxxm3:validPeriod/gml:TimePeriod/gml:endPosition')
        geometry = parser.first(f'{evolving}//iwxxm3:geometry//aixm:horizontalProjection/*[1]')
        direction_value = parser.first(f'{evolving}//iwxxm3:directionOfMotion')
        direction_unit = parser.first(f'{evolving}//iwxxm3:directionOfMotion/@uom')
        speed_value = parser.first(f'{evolving}//iwxxm3:speedOfMotion')
        speed_unit = parser.first(f'{evolving}//iwxxm3:speedOfMotion/@uom')

        evolving_condition = {
            'geometry': geometry
        }
        if parser.contains(f'{evolving}//iwxxm3:directionOfMotion'):
            evolving_condition['directionOfMotion'] = {
                'value': direction_value,
                'unit': direction_unit
            }

        if parser.contains(f'{evolving}//iwxxm3:speedOfMotion'):
            evolving_condition['speedOfMotion'] = {
                'value': speed_value,
                'unit': speed_unit
            }

        output = {
            'issueTime': issue_time,
            'issuingAirTrafficServicesUnit': issuing_unit,
            'originatingMeteorologicalWatchOffice': watch_office_id,
            'issuingAirTrafficServicesRegion': issuing_region,
            'sequenceNumber': sequence_number,
            'phenomenon': phenomenon,
            'validPeriod': {
                'start': valid_start,
                'end': valid_end
            },
            'evolvingCondition': evolving_condition
        }

        if parser.contains('//iwxxm3:cancelledReportSequenceNumber'):
            cancel_sequence_number = parser.first('//iwxxm3:cancelledReportSequenceNumber')
            cancel_valid_start = parser.first('//iwxxm3:cancelledReportValidPeriod/gml:TimePeriod/gml:beginPosition')
            cancel_valid_end = parser.first('//iwxxm3:cancelledReportValidPeriod/gml:TimePeriod/gml:endPosition')
            output['cancel'] = {
                'sequenceNumber': cancel_sequence_number,
                'validPeriod': {
                    'start': cancel_valid_start,
                    'end': cancel_valid_end
                }
            }

        return output


XSL_DOC = """\
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:iwxxm11="http://icao.int/iwxxm/1.1"
    xmlns:iwxxm21="http://icao.int/iwxxm/2.1"
    xmlns:iwxxm3="http://icao.int/iwxxm/3.0"
    xmlns:iwxxmus10="http://nws.weather.gov/schemas/IWXXM-US/1.0/Release"
    xmlns:gml="http://www.opengis.net/gml/3.2"
    xmlns:saf="http://icao.int/saf/1.1"
    xmlns:aixm="http://www.aixm.aero/schema/5.1.1"
>

    <xsl:template match="*">
    </xsl:template>

    <xsl:template match="iwxxm21:AIRMET | iwxxm21:SIGMET | iwxxm3:AIRMET | iwxxm3:SIGMET">
        <metadata>
            <issueTime>
                <xsl:value-of select=".//iwxxm21|iwxxm3:issueTime/gml:TimeInstant/gml:timePosition" />
            </issueTime>
            <issuingAirTrafficServicesUnit>
                <xsl:value-of select=".//iwxxm3:issuingAirTrafficServicesUnit//aixm:designator" />
            </issuingAirTrafficServicesUnit>
            <originatingMeteorologicalWatchOffice>
                <xsl:value-of select=".//iwxxm3:originatingMeteorologicalWatchOffice//aixm:designator" />
            </originatingMeteorologicalWatchOffice>
            <issuingAirTrafficServicesRegion>
                <xsl:value-of select=".//iwxxm3:issuingAirTrafficServicesRegion//aixm:designator" />
            </issuingAirTrafficServicesRegion>
            <sequenceNumber>
                <xsl:value-of select=".//iwxxm3:sequenceNumber" />
            </sequenceNumber>
            <phenomenon>
                <xsl:value-of select=".//iwxxm3:phenomenon/@xlink:href" />
            </phenomenon>
            <validPeriod>
                <xsl:apply-templates select=".//iwxxm3:validPeriod/gml:TimePeriod" />
            </validPeriod>
            <xsl:if test=".//iwxxm3:cancelledReportSequenceNumber">
                <cancel>
                    <sequenceNumber>
                        <xsl:value-of select=".//iwxxm3:cancelledReportSequenceNumber" />
                    </sequenceNumber>
                    <validPeriod>
                        <xsl:apply-templates select=".//iwxxm3:cancelledReportValidPeriod/gml:TimePeriod" />
                    </validPeriod>
                </cancel>
            </xsl:if>
            <xsl:apply-templates select=".//iwxxm3:AIRMETEvolvingConditionCollection | .//iwxxm3:SIGMETEvolvingConditionCollection" />
        </metadata>
    </xsl:template>

    <xsl:template match="iwxxm3:AIRMETEvolvingConditionCollection | iwxxm3:SIGMETEvolvingConditionCollection">
        <xsl:apply-templates select=".//iwxxm3:AIRMETEvolvingCondition | .//iwxxm3:SIGMETEvolvingCondition" />
    </xsl:template>

    <xsl:template match="iwxxm3:AIRMETEvolvingCondition | iwxxm3:SIGMETEvolvingCondition">
        <evolvingCondition>
            <geometry>
                <xsl:apply-templates select=".//iwxxm3:geometry//aixm:horizontalProjection/*[1]" />
            </geometry>
            <xsl:call-template name="quantitativeValue">
                <xsl:with-param name="elem" select=".//iwxxm3:directionOfMotion" />
            </xsl:call-template>
            <xsl:call-template name="quantitativeValue">
                <xsl:with-param name="elem" select=".//iwxxm3:speedOfMotion" />
            </xsl:call-template>
        </evolvingCondition>
    </xsl:template>

    <xsl:template match="aixm:ElevatedPoint">
        <gml:Point>
            <xsl:copy-of select="./@*" />
            <xsl:copy-of select="./*" />
        </gml:Point>
    </xsl:template>

    <xsl:template match="aixm:Surface">
        <gml:Surface>
            <xsl:copy-of select="./@*" />
            <xsl:copy-of select="./*" />
        </gml:Surface>
    </xsl:template>

    <xsl:template match="gml:Point">
        <xsl:copy-of select="." />
    </xsl:template>

    <xsl:template match="gml:TimePeriod">
        <start>
            <xsl:value-of select="gml:beginPosition" />
        </start>
        <end>
            <xsl:value-of select="gml:endPosition" />
        </end>
    </xsl:template>

    <xsl:template name="quantitativeValue">
        <xsl:param name="elem" />
        <xsl:if test="$elem">
            <xsl:element name="{local-name($elem)}">
                <value><xsl:value-of select="$elem" /></value>
                <unit><xsl:value-of select="$elem/@uom" /></unit>
            </xsl:element>
        </xsl:if>
    </xsl:template>

</xsl:stylesheet>"""  # noqa: E501
