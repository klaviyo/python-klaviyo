import pytest
from .fixtures.public import KlaviyoPublicFixture
from klaviyo.exceptions import (
    KlaviyoAuthenticationError, KlaviyoConfigurationException,
    KlaviyoException, KlaviyoRateLimitException,
)

class TestPublic(KlaviyoPublicFixture):

    def test_track_success(self, mock_event, mock_email, mock_public_request_success):
        response = self.public.track(mock_event, mock_email)
        assert response.data == mock_public_request_success.return_value

    def test_track_raise(self, mock_event):
        with pytest.raises(KlaviyoException):
            self.public.track(mock_event)
