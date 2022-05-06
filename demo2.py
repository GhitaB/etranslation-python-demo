""" Test eTranslation, SOAP
"""
from zeep import Client
from zeep.wsse.username import UsernameToken
from secret_config import USERNAME, PASSWORD, EMAIL
from config import SOURCE_LANGUAGE, TARGET_LANGUAGE

client = Client(
    'https://webgate.ec.europa.eu/etranslation/si/WSEndpointHandlerService?WSDL',
    wsse=UsernameToken(USERNAME, PASSWORD))
# todo get the password from ENV

client.service.translate(
    {'priority': '5',
     'external-reference': '1',
     'caller-information': {'application': 'Marine_EEA_20180706',
                            'username': 'dumitval'},
     'text-to-translate': 'Please translate this text for me.',
     'source-language': SOURCE_LANGUAGE,
     'target-languages': {'target-language': TARGET_LANGUAGE},
     'domain': 'GEN',
     'requester-callback':
         'https://wise-test.eionet.europa.eu/translation_callback',
     'destinations': {
         'http-destination':
             'https://wise-test.eionet.europa.eu/translation_callback',
         'email-destination':
             EMAIL
        }
     })
