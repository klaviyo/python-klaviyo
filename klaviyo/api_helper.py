from abc import ABCMeta
import base64
import datetime
import json
import time

import requests
import simplejson

try:
   from urllib.parse import urlencode
except ImportError:
   from urllib import urlencode

from .exceptions import (
    KlaviyoAPIException,
    KlaviyoConfigurationException,
    KlaviyoAuthenticationError, KlaviyoRateLimitException,
    KlaviyoServerError,
)
from klaviyo import __version__


class KlaviyoAPIResponse(object):
    def __init__(self, status_code, data):
        self.status_code = status_code
        self.data = data


class KlaviyoAPI(object):
    __metaclass__ = ABCMeta
    KLAVIYO_API_SERVER = 'https://a.klaviyo.com/api'
    KLAVIYO_DATA_VARIABLE = 'data'
    V1_API = 'v1'
    V2_API = 'v2'
    EMPTY_RESPONSE = ''
    API_KEY = 'api_key'

    # HTTP METHODS
    HTTP_DELETE = 'delete'
    HTTP_GET = 'get'
    HTTP_POST = 'post'
    HTTP_PUT = 'put'

    PUBLIC_API_RESPONSES = ('0', '1', )

    # TYPE OF API METHOD
    PRIVATE = 'private'
    PUBLIC = 'public'

    # UNIVERSAL KEYS
    METRIC = 'metric'
    METRICS = 'metrics'
    TIMELINE = 'timeline'

    # REQUEST PARAMS
    COUNT = 'count'
    PAGE = 'page'
    SORT = 'sort'
    PROFILES = 'profiles'
    EMAILS = 'emails'
    EMAIL = 'email'
    SINCE = 'since'
    MARKER = 'marker'

    # SORTING
    SORT_ASC = 'asc'
    SORT_DESC = 'desc'

    def __init__(self, public_token=None, private_token=None, api_server=KLAVIYO_API_SERVER):
        self.public_token = public_token
        self.private_token = private_token
        self.api_server = api_server

        # if you only need to do one type of request, it's not required to have both private and public.. but we need at least 1 token
        if not self.public_token and not self.private_token:
            raise KlaviyoConfigurationException('You must provide a public or private api token')

    ######################
    # HELPER FUNCTIONS
    ######################
    @staticmethod
    def _normalize_timestamp(timestamp):
        """Makes a datetime obj an epoch time.

        Args:
            timestamp (int or datetime): Time of what is happening.

        Returns:
            (int): Unix timestamp.
        """
        if isinstance(timestamp, datetime.datetime):
            timestamp = time.mktime(timestamp.timetuple())
        return timestamp

    @staticmethod
    def _filter_params(params):
        """Normalize all params and remove ones that don't exist.

        Args:
            params (dict): API Query params.

        Returns:
            (dict): Valid query parameters.
        """
        return dict((k, v) for k, v in params.items() if v is not None)

    def _build_marker_param(self, marker):
        """Creates a dictionary with the offset.

        Args:
            marker (int): Offset for the next request.

        Returns:
            (dict): Information containing the offset.
        """
        params = {}
        if marker:
            params[self.MARKER] = marker
        return params

    def _build_query_string(self, params, is_test):
        return urlencode({
            self.KLAVIYO_DATA_VARIABLE: base64.b64encode(json.dumps(params).encode('utf-8')),
            'test': 1 if is_test else 0,
        })

    #####################
    # API HELPER FUNCTIONS
    #####################
    def _is_valid_request_option(self, request_type=PRIVATE):
        """Making sure the appropriate credentials are passed in for the api request.

        Args:
            request_type (str): the type of method (private/public).

        Raises:
            (KlaviyoConfigurationException): Information as to why the request won't work.
        """
        if request_type == self.PUBLIC and not self.public_token:
            raise KlaviyoConfigurationException('Public token is not defined')

        if request_type == self.PRIVATE and not self.private_token:
            raise KlaviyoConfigurationException('Private token is not defined')

    def _v2_request(self, path, method, data={}):
        """Handles the v2 api requests.

        Args:
            path (str): Url we make a request to.
            method (str): HTTP method.
            data (dict): Query parameters for the api call.
        Returns:
            (dict or arr): Response from Klaviyo API.
        """

        url = '{}/{}/{}'.format(
            self.api_server,
            self.V2_API,
            path,
        )
        data.update({
            self.API_KEY: self.private_token
        })
        data = json.dumps(data)

        return self._request(method, url, data=data)

    def _v1_request(self, path, method, params={}):
        """Handles the v1 api requests.

        Args:
            path (str): Url we make a request to.
            method (str): HTTP method.
            params (dict): Query parameters for the api call.
        Returns:
            (dict or arr): Response from Klaviyo API.
        """
        url = '{}/{}/{}'.format(
            self.api_server,
            self.V1_API,
            path,
        )
        params.update({
            self.API_KEY: self.private_token
        })

        return self._request(method, url, params)

    def _public_request(self, path, querystring):
        """Track and identify calls, always a get request.

        Args:
            path (str): track or identify.
            querystring (str): urlencoded & b64 encoded string.
        Returns:
            (str): 1 or 0 (pass/fail).
        """

        url = '{}/{}?{}'.format(self.api_server, path, querystring)
        return self._request(self.HTTP_GET, url, request_type=self.PUBLIC)

    def _request(self, method, url, params=None, data=None, request_type=PRIVATE):
        """Executes the request being made.

        Args:
            method (str): Type of HTTP request.
            url (str): URL to make the request to.
            params (dict or json): Body of the request.
        Returns:
            (str, dict): Public returns 1 or 0  (pass/fail).
                        v1/v2 returns (dict, list).
        """
        self._is_valid_request_option(request_type=request_type)
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Klaviyo-Python/{}'.format(__version__)
        }
        response = getattr(requests, method.lower())(
            url,
            headers=headers,
            params=params,
            data=data
        )

        return self._handle_response(response)

    def _handle_response(self, response):
        """Handles api HTTP response and validates.

        Args:
            response (Response): Http response object.

        Returns:
            (KlaviyoApiResponse): Information about the response.

        Raises:
            (KlaviyoAuthenticationError): 403 authentication error.
            (KlaviyoRateLimitException): 429 rate limit.
            (KlaviyoServerError): 5XX Server error.
            (KlaviyoAPIException): A catch all for all other status codes.

        """
        status_code = response.status_code
        if status_code == 403:
            raise KlaviyoAuthenticationError(status_code, response)
        elif status_code == 429:
            raise KlaviyoRateLimitException(status_code, response)
        elif status_code in (500, 503, ):
            raise KlaviyoServerError(status_code, response)
        elif status_code != 200 and status_code != 202:
            raise KlaviyoAPIException(status_code, response)

        return self._handle_successful_response(response, status_code)

    def _handle_successful_response(self, response, status_code):
        """Determines how to handle a 20X http response.

        Args:
            response (obj): Requests object.
            status_code (int): HTTP status code.

        Returns:
            (KlaviyoApiResponse): Information about the response.
        """
        try:
            return KlaviyoAPIResponse(status_code, response.json())
        except (simplejson.JSONDecodeError, ValueError) as e:
            # it's kinda bad that we just do this, but need to return if it's a 200
            if response.text == self.EMPTY_RESPONSE or response.text in self.PUBLIC_API_RESPONSES:
                return KlaviyoAPIResponse(status_code, response.text)
            else:
                raise KlaviyoAPIException(
                    message='Request did not return json: {}'.format(e),
                    status_code=status_code,
                    response=response
               )

