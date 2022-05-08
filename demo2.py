""" Test eTranslation, SOAP
"""
from zeep import Client
from zeep.wsse.username import UsernameToken
from secret_config import USERNAME, PASSWORD, EMAIL
from config import SOURCE_LANGUAGE, TARGET_LANGUAGE
import base64

with open("./files/test-file.html", "rb") as html_file:
    encoded_file = base64.b64encode(html_file.read())

client = Client(
    'https://webgate.ec.europa.eu/etranslation/si/WSEndpointHandlerService?WSDL',
    wsse=UsernameToken(USERNAME, PASSWORD))
# todo get the password from ENV

response = client.service.translate(
    {'priority': '5',
     'external-reference': '1',
     'caller-information': {'application': 'Marine_EEA_20180706',
                            'username': 'dumitval'},
     # 'text-to-translate': 'Please translate this text for me.',

     "document-to-translate-base64" : {
        "content" : encoded_file,
        "format" : "html",
        "fileName" : "out"
     },

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

# If the response is a negative number this means error. The list of error codes here:
# https://ec.europa.eu/cefdigital/wiki/display/CEFDIGITAL/How+to+submit+a+translation+request+via+the+CEF+eTranslation+webservice
import pdb; pdb.set_trace()
