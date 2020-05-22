from .api_helper import KlaviyoAPI
from .exceptions import KlaviyoException

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
        id=None,
        properties=None,
        customer_properties=None,
        timestamp=None,
        ip_address=None,
        is_test=False
        ):
        """Will create an event (metric) in Klaviyo.

        Args:
            event (str): Event name to be tracked.
            email (str or None): Email address.
            id (str or None): External id for customer.
            properties (dict): Information about the event.
            customer_properties (dict): Information about the customer.
            timestamp (unix timestamp): Time the request is happening.
            ip_address (str): Ip address of the customer.
            is_test (bool): Should this be a test request.

        Returns:
            (str): 1 (pass) or 0 (fail).
        """
        if not email and not id:
            raise KlaviyoException(self.ERROR_MESSAGE_ID_AND_EMAIL)

        if properties is None:
            properties = {}
        
        if customer_properties is None:
            customer_properties = {}

        if email: 
            customer_properties['email'] = email

        if id: 
            customer_properties['id'] = id

        params = {
            self.TOKEN: self.public_token,
            'event': event,
            'properties': properties,
            'customer_properties': customer_properties,
            'time': self._normalize_timestamp(timestamp),
        }

        if ip_address:
            params['ip'] = ip_address

        query_string = self._build_query_string(params, is_test)
        return self._public_request(self.TRACK, query_string)

    def track_once(
        self, 
        event, 
        email=None, 
        id=None, 
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
            id (str or None): External id for customer.
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

        return self.track(event, email=email, id=id, properties=properties, customer_properties=customer_properties,
            ip_address=ip_address, is_test=is_test)

    def identify(self, email=None, id=None, properties={}, is_test=False):
        """Makes an identify call to Klaviyo API.
        This will create/update a user with its associated customer properties.

        Args:
            email (str or None): Email address.
            id (str or None): External id for customer.
            properties (dict): Information about the customer.
            is_test (bool): Should this be a test request.
        Returns:
            (str): 1 (pass) or 0 (fail)
        """
        if email is None and id is None:
            raise KlaviyoException('You must identify a user by email or ID.')

        if not isinstance(properties, dict):
            properties = {}

        if email: properties['email'] = email
        if id: properties['id'] = id

        query_string = self._build_query_string({
            self.TOKEN: self.public_token,
            'properties': properties,
        }, is_test)

        return self._public_request(self.IDENTIFY, query_string)
