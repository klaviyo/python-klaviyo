from .api_helper import KlaviyoAPI
from .exceptions import KlaviyoException

class DataPrivacy(KlaviyoAPI):
    DATA_PRIVACY = 'data-privacy'
    DELETION_REQUEST = 'deletion-request'
    ALLOWED_ID_TYPES = [
        'email',
        'phone_number',
        'person_id',
    ]

    def request_profile_deletion(self, identifier, id_type='email'):
        """Request a data privacy-compliant deletion for the person record corresponding to an email address,
        phone number, or person identifier. If multiple person records exist for the provided identifier,
        only one of them will be deleted.

        https://www.klaviyo.com/docs/api/v2/data-privacy#post-deletion-request

        Args:
            identifier (str): The email address, phone number in E.164 format, or person_id corresponding to a person record to delete.
            id_type (str): The type of identifier provided, can be one of: 'email', 'phone_number', or 'person_id'.
        Returns:
            (KlaviyoAPIResponse): Object with HTTP response code and data.
        Raises:
            (KlaviyoAPIException): Raised if invalid id_type is provided.
        """
        if id_type not in self.ALLOWED_ID_TYPES:
            raise KlaviyoException('Invalid id_type provided. Valid types are: {}'.format(self.ALLOWED_ID_TYPES))

        data = {
            id_type: identifier,
        }

        return self._v2_request('{}/{}'.format(self.DATA_PRIVACY, self.DELETION_REQUEST), self.HTTP_POST, data=data)
        
