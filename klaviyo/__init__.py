import urllib
import base64
import json

import requests

KLAVIYO_API_SERVER = 'a.klaviyo.com'
KLAVIYO_TRACKING_ENDPOINT = 'api/track'
KLAVIYO_IDENTIFY_ENDPOINT = 'api/identify'
KLAVIYO_DATA_VARIABLE = 'data'

TRACK_ONCE_KEY = '__track_once__'

class KlaviyoException(Exception):
    pass

class Klaviyo(object):
    
    def __init__(self, api_token, api_server=KLAVIYO_API_SERVER):
        self.api_token = api_token
        self.api_server = api_server
    
    def track(self, event, email=None, id=None, properties=None, customer_properties=None,
        timestamp=None, ip_address=None, is_test=False):
        
        if email is None and id is None:
            raise KlaviyoException('You must identify a user by email or ID.')
        
        if properties is None:
            properties = {}
        
        if customer_properties is None:
            customer_properties = {}
        
        if email: customer_properties['email'] = email
        if id: customer_properties['id'] = id
        
        url_params = self._build_params({
            'token' : self.api_token,
            'event' : event,
            'properties' : properties,
            'customer_properties' : customer_properties,
            'time' : timestamp,
            'ip' : ip_address or '',
        }, is_test)
        return self._request(KLAVIYO_TRACKING_ENDPOINT, url_params)
    
    def track_once(self, event, email=None, id=None, properties=None, customer_properties=None,
        timestamp=None, ip_address=None, is_test=False):
        
        if properties is None:
            properties = {}
        
        properties[TRACK_ONCE_KEY] = True
        
        return self.track(event, email=email, id=id, properties=properties, customer_properties=customer_properties,
            ip_address=ip_address, is_test=is_test)
    
    def identify(self, email=None, id=None, properties=None, is_test=False):
        if email is None and id is None:
            raise KlaviyoException('You must identify a user by email or ID.')
        
        if properties is None:
            properties = {}
        
        if email: properties['email'] = email
        if id: properties['id'] = id
        
        url_params = self._build_params({
            'token' : self.api_token,
            'properties' : properties,
        }, is_test)
        return self._request(KLAVIYO_IDENTIFY_ENDPOINT, url_params)
    
    def _build_params(self, params, is_test):
        return urllib.urlencode({
            KLAVIYO_DATA_VARIABLE : base64.b64encode(json.dumps(params)),
            'test' : 1 if is_test else 0,
        })

    def _request(self, path, params):
        server = self.api_server
        response = requests.get('http://%s/%s?%s' % (server, path, params))
        
        return response.text == '1'
