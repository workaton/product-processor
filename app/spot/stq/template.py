from __future__ import absolute_import

import logging
from datetime import datetime
from textwrap import TextWrapper

from jinja2 import Environment, FileSystemLoader, PackageLoader, Template
from jinja2.ext import Extension

class TemplateEngine(object):
    '''Creates documents based on templates.

    The custom extensions in this module will be loaded automatically into the
    initialized Jinja environment.

    '''

    standard_extensions = set()

    @classmethod
    def extension(cls, extension):
        '''Decorator for adding extensions to the default environment.'''

        cls.standard_extensions.add(extension)

    def __init__(self, base_directory=None, **kwargs):
        '''Initializes a template environment.

        :param base_directory: base directory for templates

        '''
        env_args = dict(kwargs)
        self.__logger = logging.getLogger(__name__)

        # Set some defaults
        if "loader" not in env_args:
            if base_directory:
                env_args["loader"] = FileSystemLoader(base_directory)
            else:
                env_args["loader"] = PackageLoader("app") # HERE MODULE NOT LOADING
        if "trim_blocks" not in env_args:
            env_args["trim_blocks"] = True
        if "extensions" not in env_args:
            env_args["extensions"] = []
        env_args["extensions"] += self.standard_extensions
        
        self.__logger.debug("Template engine initializing")
        self.env = Environment(**env_args)
        self.env.globals["now"] = lambda: datetime()
        self.__logger.debug("Template engine initialized")

    def render(self, template_name, template_args):
        self.__logger.debug('Rendering template "{0}" with data: {1}'.format(template_name, template_args))
        template = self.env.get_template(template_name)

        return template.render(template_args)


@TemplateEngine.extension
class DatetimeExtension(Extension):
    ''' Jinja2 extension for formatting a datetime object '''

    def __init__(self, environment):
        environment.filters['datetime'] = self.filter_datetime
        super(self.__class__, self).__init__(environment)

    def filter_datetime(self, value, format="%Y-%m-%d %H:%M:%S"):
        if value:
            value = datetime.strptime(value,"%Y-%m-%d %H:%M:%S")
            return value.strftime(format)
        else:
            return ""


@TemplateEngine.extension
class JustifyExtension(Extension):
    ''' Jinja2 extension for left and right justification of strings '''

    def __init__(self, environment):
        environment.filters['left'] = self.filter_left
        environment.filters['right'] = self.filter_right
        super(self.__class__, self).__init__(environment)

    def filter_left(self, s, width, truncate=True):
        if s is None:
            return ""

        if truncate:
            return s.ljust(width)[:width]
        else:
            return s.ljust(width)

    def filter_right(self, s, width, truncate=True):
        if s is None:
            return ""

        if truncate:
            return s.rjust(width)[:width]
        else:
            return s.rjust(width)


@TemplateEngine.extension
class KeyvaluesExtension(Extension):
    ''' Jinja2 extension for turning dictionaries into key-value pair strings

    This converts a dictionary into a list of key-value pair strings like so:

    { "a": "Test", "b": "Another" } --> ["a=Test", "b=Another"]

    '''

    def __init__(self, environment):
        environment.filters['keyvalues'] = self.filter_keyvalues
        super(self.__class__, self).__init__(environment)

    def filter_keyvalues(self, dictionary):
        return ["{0}={1}".format(key, value)
                for key, value in dictionary.items()]

@TemplateEngine.extension
class LinewrapExtension(Extension):
    ''' Jinja2 extension for wrapping long lines

    This is necessary since the width of the wordwrap filter is a minimum
    when break_long_words is False.  We want it to be a maximum.

    '''

    def __init__(self, environment):
        environment.filters['linewrap'] = self.filter_linewrap
        super(self.__class__, self).__init__(environment)

    def filter_linewrap(self, s, width, indent=0):
        wrapper = TextWrapper(width=width, break_on_hyphens=False)
        return ("\n" + " " * indent).join(wrapper.wrap(s))
