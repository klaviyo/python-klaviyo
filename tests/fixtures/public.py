from mock import patch
import pytest
from klaviyo.public import Public
from .api_helper import KlaviyoAPIFixture

class PublicFixture(KlaviyoAPIFixture):
    @property
    def api(self):
        return Public(**self.API_SETTINGS)

    @pytest.fixture
    def mock_email(self):
        return 'thomas.jefferson@mailinator.com'

    @pytest.fixture
    def mock_valid_id_type(self):
        return 'email'

    @pytest.fixture
    def mock_invalid_id_type(self):
        return 'pizza'

    @pytest.fixture
    def mock_external_id(self):
        return 123
