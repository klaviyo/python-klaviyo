from .api_helper import KlaviyoAPI, KlaviyoAPIResponse
from .exceptions import KlaviyoException
from json import dumps
from requests import request
try:
   from urllib.parse import quote
except ImportError:
   from urllib import quote

class Public(KlaviyoAPI):
    # PUBLIC API PATHS
    IDENTIFY = 'identify'
    TRACK = 'track'
    TRACK_ONCE_KEY = '__track_once__'

    TOKEN = 'token'
    ERROR_MESSAGE_ID_AND_EMAIL = 'You must identify a user by email or ID.'

    def track(
        self,
        event,
        email=None,
        external_id=None,
        properties=None,
        customer_properties=None,
        timestamp=None,
        ip_address=None,
        is_test=False,
        method=KlaviyoAPI.HTTP_GET
        ):
        """Will create an event (metric) in Klaviyo.

        https://www.klaviyo.com/docs/http-api#track

        Args:
            event (str): Event name to be tracked.
            email (str or None): Email address.
            external_id (str or None): External id for customer.
            properties (dict): Information about the event.
            customer_properties (dict): Information about the customer.
            timestamp (unix timestamp): Time the request is happening.
            ip_address (str): Ip address of the customer.
            is_test (bool): Should this be a test request.
            method (str): 'post' or 'get'. Defaults to 'get'. We recommend 'post', but support 'get' for backwards compatibility.

        Returns:
            (str): 1 (pass) or 0 (fail).
        """

        self._valid_identifiers(email, external_id)

        if properties is None:
            properties = {}
        
        if customer_properties is None:
            customer_properties = {}

        if email: 
            customer_properties['email'] = email

        if external_id: 
            customer_properties['id'] = external_id

        params = {
            self.TOKEN: self.public_token,
            'event': event,
            'properties': properties,
            'customer_properties': customer_properties,
            'time': self._normalize_timestamp(timestamp),
        }

        if ip_address:
            params['ip'] = ip_address

        if method.lower() not in ['get','post']:

            raise ValueError('method argument must be either "post" or "get"')

        if method == 'post':

            url = '{}/{}'.format(KlaviyoAPI.KLAVIYO_API_SERVER,self.TRACK)

            headers = {
                "Accept": "text/html",
                "Content-Type": "application/x-www-form-urlencoded"
            }

            datastring = self._build_data_string(params)

            return self._public_post_request(url, datastring, headers)

        else: # original 'get' case

            query_string = self._build_query_string(params, is_test)
            return self._public_request(self.TRACK, query_string)

    def track_once(
        self, 
        event, 
        email=None, 
        external_id=None, 
        properties=None, 
        customer_properties=None,
        timestamp=None, 
        ip_address=None, 
        is_test=False
        ):
        """
        Args:
            event (str): Event name to be tracked.
            email (str or None): Email address.
            external_id (str or None): External id for customer.
            properties (dict): Information about the event.
            customer_properties (dict): Information about the customer.
            timestamp (unix timestamp): Time the request is happening.
            ip_address (str): Ip address of the customer.
            is_test (bool): Should this be a test request.

        Returns:
            (str): 1 (pass) or 0 (fail).
        """
        if properties is None:
            properties = {}

        properties[self.TRACK_ONCE_KEY] = True

        return self.track(event, email=email, external_id=external_id, properties=properties, customer_properties=customer_properties,
            timestamp=timestamp, ip_address=ip_address, is_test=is_test)

    def identify(self, email=None, external_id=None, properties={}, is_test=False, method=KlaviyoAPI.HTTP_GET):
        """Makes an identify call to Klaviyo API.

        This will create/update a user with its associated customer properties.
        https://www.klaviyo.com/docs/http-api#identify

        Args:
            email (str or None): Email address.
            external_id (str or None): External id for customer.
            properties (dict): Information about the customer.
            is_test (bool): Should this be a test request.
            method (str): 'post' or 'get'. Defaults to 'get'. We recommend 'post', but support 'get' for backwards compatibility.

        Returns:
            (str): 1 (pass) or 0 (fail).
        """
        self._valid_identifiers(email, external_id)

        if not isinstance(properties, dict):
            properties = {}

        if email:
            properties['email'] = email

        if external_id:
            properties['id'] = external_id

        params = {
            self.TOKEN: self.public_token,
            'properties': properties
        }


        if method.lower() not in ['get','post']:

            raise ValueError('method argument must be either "post" or "get"')

        if method == 'post':

            url = '{}/{}'.format(KlaviyoAPI.KLAVIYO_API_SERVER,self.IDENTIFY)

            headers = {
                "Accept": "text/html",
                "Content-Type": "application/x-www-form-urlencoded"
            }

            datastring = self._build_data_string(params)

            return self._public_post_request(url, datastring, headers)

        else: # original 'get' case

            query_string = self._build_query_string(params, is_test)
            return self._public_request(self.IDENTIFY, query_string)

    @staticmethod
    def _valid_identifiers(email=None, external_id=None):
        """Checks whether we can identify a profile using an email or external id.

        Args:
            email (str or None): Email address.
            external_id (str or None): External id for customer.
        Raises:
            (KlaviyoException): Identifiers not provided.
        """
        if not email and not external_id:
            raise KlaviyoException(Public.ERROR_MESSAGE_ID_AND_EMAIL)

