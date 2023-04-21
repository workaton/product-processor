from __future__ import annotations

from ngitws.types import MediaType


class MediaTypes:

    APPLICATION_IWXXM_US_XML = MediaType('application', 'vnd.noaa.iwxxm-us+xml')
    APPLICATION_IWXXM_XML = MediaType('application', 'vnd.wmo.iwxxm+xml')
    APPLICATION_JSON = MediaType('application', 'json')
    APPLICATION_OCTET_STREAM = MediaType('application', 'octet-stream')
    APPLICATION_USWX_XML = MediaType('application', 'vnd.noaa.uswx+xml')
    IMAGE_G3FAX = MediaType('image', 'g3fax')
    IMAGE_PNG = MediaType('image', 'png')
    TEXT_CSV = MediaType('text', 'csv')
    TEXT_PLAIN = MediaType('text', 'plain')
