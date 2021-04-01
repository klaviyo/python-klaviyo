from mock import patch
import pytest
from klaviyo.data_privacy import DataPrivacy
from .api_helper import KlaviyoAPIFixture

class DataPrivacyFixture(KlaviyoAPIFixture):
    @property
    def api(self):
        return DataPrivacy(**self.API_SETTINGS)

    @pytest.fixture
    def mock_identifier(self):
        return 'thomas.jefferson@mailinator.com'

    @pytest.fixture
    def mock_valid_id_type(self):
        return 'email'

    @pytest.fixture
    def mock_invalid_id_type(self):
        return 'pizza'
