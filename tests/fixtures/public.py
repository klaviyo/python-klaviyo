from mock import patch
import pytest
from tests.fixtures.api_helper import KlaviyoAPIFixture

from klaviyo.public import Public

class KlaviyoPublicFixture(KlaviyoAPIFixture):

    @property
    def public(self):
        return Public(public_token=self.API_SETTINGS['public_token'])

    @pytest.fixture
    def mock_event(self):
        return 'Started Checkout'

    @pytest.fixture
    def mock_email(self):
        return 'fred.flintstone@klaviyo.com'

    @pytest.fixture
    def mock_public_request_success(self):
        with patch.object(self.public, self.public.track.__name__) as mock_request:
            mock_request.return_value = 1
            yield mock_request
