import pytest
from .fixtures.public import PublicFixture
from klaviyo.exceptions import (
    KlaviyoException
)


class TestPublicApi(PublicFixture):
    def test_identify_with_id(self, mock_email, mock_external_id, mock_request):
        self.api.identify(mock_email, mock_external_id)
        mock_request.assert_called_once()

    def test_identify_without_id(self, mock_email, mock_request):
        self.api.identify(mock_email)
        mock_request.assert_called_once()

    def test_identify_without_identification(self):
        with pytest.raises(KlaviyoException):
            self.api.identify()
