import pytest
from .fixtures.api_helper import KlaviyoAPIFixture
from klaviyo.exceptions import (
    KlaviyoAuthenticationError, KlaviyoConfigurationException,
    KlaviyoRateLimitException,
)


class TestKlaviyoAPI(KlaviyoAPIFixture):

    def test_filter_params(self, mock_params):
        params = self.api._filter_params(mock_params)
        assert (
            all(params.values()) and
            params[self.api.COUNT] == 1
        )

    def test_build_marker_param(self, mock_marker_param):
        params = self.api._build_marker_param(mock_marker_param)
        assert params[self.api.MARKER] == 2000

    def test_build_query_string(self, mock_params):
        query_string = self.api._build_query_string(mock_params, False)
        assert (
            isinstance(query_string, str) and
            '&' in query_string
        )

    def test_is_valid_request_option_private(self):
        with pytest.raises(KlaviyoConfigurationException):
            self.api_no_private_token._is_valid_request_option()

    def test_v2_request(self, mock_lists_path, mock_get_method, mock_params, mock_request, mock_handle_response):
        self.api._v2_request(mock_lists_path, mock_get_method, mock_params)
        mock_request.assert_called_once()

    def test_v1_request(self, mock_lists_path, mock_get_method, mock_params, mock_request, mock_handle_response):
        self.api._v1_request(mock_lists_path, mock_get_method, mock_params)
        mock_request.assert_called_once()

    def test_public_request(self, mock_lists_path, mock_querystring, mock_request):
        self.api._public_request(mock_lists_path, mock_querystring)
        mock_request.assert_called_once()

    def test_request(self, mock_get_method, mock_url, mock_requests_package, mock_handle_response):
        self.api._request(mock_get_method, mock_url)
        mock_requests_package.assert_called_once()

    def test_handle_response_with_auth_error(self, mock_response_auth_error, mock_request_type_private):
        with pytest.raises(KlaviyoAuthenticationError):
            self.api._handle_response(mock_response_auth_error)

    def test_handle_response_with_rate_limit_error(self, mock_response_rate_limit_error, mock_request_type_private):
        with pytest.raises(KlaviyoRateLimitException):
            self.api._handle_response(mock_response_rate_limit_error)
