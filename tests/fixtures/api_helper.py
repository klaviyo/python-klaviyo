from mock import MagicMock, patch
import pytest
import requests
from klaviyo.api_helper import KlaviyoAPI

class KlaviyoAPIFixture:
    API_SETTINGS = {
        'public_token': 'qw123qw123qw123',
        'private_token': 'pk_flintstones'
    }

    @property
    def api(self):
        return KlaviyoAPI(**self.API_SETTINGS)

    @property
    def api_no_private_token(self):
        return KlaviyoAPI(public_token=self.API_SETTINGS['public_token'])

    @pytest.fixture
    def mock_params(self):
        return {
            self.api.COUNT: 1,
            self.api.SORT: self.api.SORT_ASC
        }

    @pytest.fixture
    def mock_marker_param(self):
        return 2000

    @pytest.fixture
    def mock_request(self):
        with patch.object(KlaviyoAPI, KlaviyoAPI._request.__name__) as mock_request:
            yield mock_request

    @pytest.fixture
    def mock_handle_response(self):
        with patch.object(KlaviyoAPI, KlaviyoAPI._handle_response.__name__) as mock_handle_response:
            yield mock_handle_response

    @pytest.fixture
    def mock_lists_path(self):
        return 'lists'

    @pytest.fixture
    def mock_get_method(self):
        return self.api.HTTP_GET

    @pytest.fixture
    def mock_querystring(self):
        return self.api._build_query_string(
            self.mock_track_request(),
            True
        )

    def mock_track_request(self):
        return {
            "token": "AB00CD",
            "event": "Elected President",
            "customer_properties": {
                "$email": "thomas.jefferson@example.com"
            },
            "properties": {
                "PreviouslyVicePresident": True,
                "YearElected": 1801,
                "VicePresidents": ["Aaron Burr", "George Clinton"]
            },
            "time": 1589983886
        }

    @pytest.fixture
    def mock_requests_package(self):
        with patch.object(requests, requests.get.__name__) as mock_requests_package:
            yield mock_requests_package


    @pytest.fixture
    def mock_url(self):
        return 'https://a.klaviyo.com/api/v2/lists'

    @pytest.fixture
    def mock_response_auth_error(self):
        return self.mock_response(
            403,
            self.api.PRIVATE
        )

    @pytest.fixture
    def mock_response_rate_limit_error(self):
        return self.mock_response(
            429,
            self.api.PRIVATE
        )

    @pytest.fixture
    def mock_request_type_private(self):
        return self.api.PRIVATE

    def mock_response(self, status_code, headers=None, json={}):
        """Mock and HTTP Request response.

        Args:
            status_code (int): HTTP status code.
            headers (dict): HTTP response headers.
            json (dict): Api response.

        Returns:
            (MagicMock): Information about a mocked request for testing.
        """
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.headers = headers
        mock_response.json = MagicMock(return_value=json)

        return mock_response
