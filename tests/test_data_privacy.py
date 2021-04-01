import pytest
from .fixtures.data_privacy import DataPrivacyFixture
from klaviyo.exceptions import (
    KlaviyoException
)

class TestDataPrivacy(DataPrivacyFixture):
    def test_request_profile_deletion(self, mock_identifier, mock_valid_id_type, mock_request):
        self.api.request_profile_deletion(mock_identifier, mock_valid_id_type)
        mock_request.assert_called_once()

    def test_request_profile_deletion_failure(self, mock_identifier, mock_invalid_id_type):
        with pytest.raises(KlaviyoException):
            self.api.request_profile_deletion(mock_identifier, mock_invalid_id_type)
