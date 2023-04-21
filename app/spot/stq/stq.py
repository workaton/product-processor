import logging
#import md5
import os
import os.path
import pytz
import shutil
import tempfile
from datetime import datetime
from subprocess import check_output, STDOUT, CalledProcessError
from textwrap import TextWrapper
from time import sleep, time

class StqApp(object):
    '''STQ daemon application.'''

    def __init__(
        self,
        generator,
        provider,
    ):
        self.generator = generator
        self.provider = provider
        self.closing = False
        self.__Product = None

        self.__logger = logging.getLogger(__name__)


    def run(self):
        self.closing = False

        while not self.closing:
            try:
                start_time = time()

                try:
                    self.main()
                except KeyboardInterrupt:
                    raise
                except:
                    self.__logger.exception('Error occurred in main program loop')

                # wait_time = start_time + self.polling_interval - time()
                # if not self.closing and wait_time > 0:
                #     sleep(wait_time)
            except KeyboardInterrupt:
                self.__logger.info('Received keyboard interrupt -- shutting down')
                self.closing = True

        self.__logger.info('Exiting program')

    def shutdown(self):
        self.__logger.info('Received shutdown signal')
        self.closing = True

    def main(self):
        '''Creates STQ product for request and updates SPOT tables.'''

        requests = []

        try:
            requests = self.provider
            self.shutdown()
            # Fetch any new requests
            if not requests:
                self.__logger.debug('No new requests found')
            else:
                self.__logger.info('{0} new request(s) found'.format(len(requests)))
                for request in requests:
                    try:
                        self.handle_request(request)
                    except:
                        self.__logger.exception(
                            'Unexpected error processing request {0}.{1}'
                            .format(request['id'], request['update'])
                        )
        except Exception as e:
            self.__logger.exception('Unexpected error retrieving pending requests')

    def handle_request(self, request):
        '''Handle a single request.'''

        _msg = 'Action {0} for request {1}.{2} ({3}) to {4}'.format(
            request['action'].upper(),
            request['id'],
            request['update'],
            request['project_name'],
            request['site'])

        self.__logger.info(_msg)

        self.__Product = self.generator.render(request)
    
    def get_product(self):
            return self.__Product

class StqProductGenerator(object):

    def __init__(self, template_engine):
        self.__template_engine = template_engine
        self.__logger = logging.getLogger(__name__)

    def render(self, request):

        result = self.__template_engine.render('product.stq', request)

        # Ensure that no lines exceed 69 characters
        wrapper = TextWrapper(
            width=69,
            replace_whitespace=False,
            drop_whitespace=True,
            break_long_words=False,
            break_on_hyphens=False
        )

        product_lines = []
        for line in result.splitlines():
            product_lines += wrapper.wrap(line) or ['']

        # Lines of a text product must end in <cr><cr><lf> as described in the
        # NWS Text Product Formats and Codes directive:
        # http://www.nws.noaa.gov/directives/sym/pd01017001curr.pdf
        product_text = '\r\r\n'.join(product_lines)
        self.__logger.debug('Created STQ product ({0} lines)\n{1}'.format(
            len(product_lines), product_text
        ))
        return StqProduct(product_text, request)


class StqProduct(object):

    def __init__(self, body, request):
        self.body = body
        self.site = request['site']
        self.id = request['id']
        self.update = request['update']
        self.submit_time = request['submit_time']


PILS = {
    'ABQ': 'ABQSTQABQ',
    'ABR': 'FSDSTQABR',
    'AER': 'ANCSTQAER',
    'AFG': 'FAISTQAFG',
    'AJK': 'JNUSTQAJK',
    'AKQ': 'WBCSTQAKQ',
    'ALU': 'ANCSTQALU',
    'ALY': 'ALBSTQALY',
    'AMA': 'LBBSTQAMA',
    'APX': 'ARBSTQAPX',
    'ARX': 'MKESTQARX',
    'BGM': 'ALBSTQBGM',
    'BIS': 'BISSTQBIS',
    'BMX': 'BHMSTQBMX',
    'BOI': 'BOISTQBOI',
    'BOU': 'DENSTQBOU',
    'BOX': 'BOSSTQBOX',
    'BRO': 'SATSTQBRO',
    'BTV': 'ALBSTQBTV',
    'BUF': 'BUFSTQBUF',
    'BYZ': 'GTFSTQBYZ',
    'CAE': 'CAESTQCAE',
    'CAR': 'PWMSTQCAR',
    'CHS': 'CAESTQCHS',
    'CLE': 'CLESTQCLE',
    'CRP': 'SATSTQCRP',
    'CTP': 'PHLSTQCTP',
    'CYS': 'CYSSTQCYS',
    'DDC': 'TOPSTQDDC',
    'DLH': 'MSPSTQDLH',
    'DMX': 'DSMSTQDMX',
    'DTX': 'ARBSTQDTX',
    'DVN': 'DSMSTQDVN',
    'EAX': 'STLSTQEAX',
    'EKA': 'SFOSTQEKA',
    'EPZ': 'LBBSTQEPZ',
    'EWX': 'SATSTQEWX',
    'FFC': 'ATLSTQFFC',
    'FGF': 'BISSTQFGF',
    'FGZ': 'PHXSTQFGZ',
    'FSD': 'FSDSTQFSD',
    'FWD': 'FTWSTQFWD',
    'GGW': 'GTFSTQGGW',
    'GID': 'OMASTQGID',
    'GJT': 'DENSTQGJT',
    'GLD': 'TOPSTQGLD',
    'GRB': 'MKESTQGRB',
    'GRR': 'ARBSTQGRR',
    'GSP': 'CAESTQGSP',
    'GUM': 'GUMSTQGUM',
    'GYX': 'PWMSTQGYX',
    'HFO': 'HFOSTQHFO',
    'HGX': 'SATSTQHGX',
    'HNX': 'SFOSTQHNX',
    'HUN': 'BHMSTQHUN',
    'ICT': 'TOPSTQICT',
    'ILM': 'RDUSTQILM',
    'ILN': 'CLESTQILN',
    'ILX': 'CHISTQILX',
    'IND': 'INDSTQIND',
    'IWX': 'INDSTQIWX',
    'JAN': 'JANSTQJAN',
    'JAX': 'MIASTQJAX',
    'JKL': 'SDFSTQJKL',
    'KEY': 'MIASTQKEY',
    'LBF': 'OMASTQLBF',
    'LCH': 'NEWSTQLCH',
    'LIX': 'NEWSTQLIX',
    'LKN': 'RNOSTQLKN',
    'LMK': 'SDFSTQLMK',
    'LOT': 'CHISTQLOT',
    'LOX': 'LAXSTQLOX',
    'LSX': 'STLSTQLSX',
    'LUB': 'LBBSTQLUB',
    'LWX': 'WBCSTQLWX',
    'LZK': 'LITSTQLZK',
    'MAF': 'LBBSTQMAF',
    'MEG': 'MEMSTQMEG',
    'MFL': 'MIASTQMFL',
    'MFR': 'PDXSTQMFR',
    'MHX': 'RDUSTQMHX',
    'MKX': 'MKESTQMKX',
    'MLB': 'MIASTQMLB',
    'MOB': 'BHMSTQMOB',
    'MPX': 'MSPSTQMPX',
    'MQT': 'ARBSTQMQT',
    'MRX': 'MEMSTQMRX',
    'MSO': 'GTFSTQMSO',
    'MTR': 'SFOSTQMTR',
    'OAX': 'OMASTQOAX',
    'OHX': 'MEMSTQOHX',
    'OKX': 'NYCSTQOKX',
    'OTX': 'SEASTQOTX',
    'OUN': 'OKCSTQOUN',
    'PAH': 'SDFSTQPAH',
    'PBZ': 'PITSTQPBZ',
    'PDT': 'PDXSTQPDT',
    'PHI': 'PHLSTQPHI',
    'PIH': 'BOISTQPIH',
    'PQR': 'PDXSTQPQR',
    'PSR': 'PHXSTQPSR',
    'PUB': 'DENSTQPUB',
    'RAH': 'RDUSTQRAH',
    'REV': 'RNOSTQREV',
    'RIW': 'CYSSTQRIW',
    'RLX': 'CRWSTQRLX',
    'RNK': 'WBCSTQRNK',
    'SEW': 'SEASTQSEW',
    'SGF': 'STLSTQSGF',
    'SGX': 'LAXSTQSGX',
    'SHV': 'NEWSTQSHV',
    'SJT': 'LBBSTQSJT',
    'SJU': 'SJUSTQSJU',
    'SLC': 'SLCSTQSLC',
    'STO': 'SFOSTQSTO',
    'TAE': 'MIASTQTAE',
    'TBW': 'MIASTQTBW',
    'TFX': 'GTFSTQTFX',
    'TOP': 'TOPSTQTOP',
    'TSA': 'OKCSTQTSA',
    'TWC': 'PHXSTQTWC',
    'UNR': 'FSDSTQUNR',
    'VEF': 'RNOSTQVEF'
}
