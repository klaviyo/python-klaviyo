import sys

from .data_privacy import DataPrivacy
from .lists import Lists
from .metrics import Metrics
from .profiles import Profiles
from .public import Public
from .campaigns import Campaigns


class Klaviyo(object):
    def __init__(self, public_token=None, private_token=None):
        self.public_token = public_token
        self.private_token = private_token

    def __getattr__(self, item):
        return KlaviyoAPIDynamicWrapper(item, self)


class KlaviyoAPIDynamicWrapper(object):
    def __init__(self, resource_class, api, *args, **kwargs):
        """An API Wrapper to dynamically load the class and method."""
        if isinstance(resource_class, str):
            self.resource_class = self.str_to_class(resource_class, api)
        else:
            self.resource_class = resource_class

    def __getattr__(self, item):
        """Overwrite to make us dynamically call the called class and its method automatically."""
        return lambda *args, **kwargs: getattr(self.resource_class, item)(*args, **kwargs)

    @classmethod
    def str_to_class(cls, str, api):
        """Transforms a string class name into a class object.
        Assumes that the class is already loaded.

        Args:
            str (str): Name of a class.
            api (obj): Klaviyo api object.

        Returns:
            (obj): KlaviyoApi resource.
        """
        return getattr(sys.modules[__name__], str)(public_token=api.public_token, private_token=api.private_token)

