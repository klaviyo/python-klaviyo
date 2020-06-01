import simplejson


class KlaviyoException(Exception):
    def __init__(self, message):
        super(KlaviyoException, self).__init__(message)
        self.message = message


class KlaviyoConfigurationException(KlaviyoException):
    pass


class KlaviyoAPIException(Exception):
    def __init__(self, status_code, response):
        super(KlaviyoAPIException, self).__init__('Failed with status code: {}'.format(status_code))
        self.status_code = status_code
        self.response = response
        self.message = self._process_message(response)

    def _process_message(self, response):
        """Creates the message attribute based on the response.

        Args:
            response (Response obj): Information about the HTTP Response.

        Returns:
            A dict or text of the response failure.
        """
        message = str()
        try:
            message = response.json()
        except (simplejson.JSONDecodeError, ValueError) as e:
            message = response.text
        return message


class KlaviyoAuthenticationError(KlaviyoAPIException):
    pass


class KlaviyoRateLimitException(KlaviyoAPIException):
    pass


class KlaviyoServerError(KlaviyoAPIException):
    pass

