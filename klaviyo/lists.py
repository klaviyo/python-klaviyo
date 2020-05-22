from .api_helper import KlaviyoAPI


class Lists(KlaviyoAPI):
    LIST = 'list'
    LISTS = 'lists'
    SUBSCRIBE = 'subscribe'
    MEMBERS = 'members'
    ALL = 'all'
    LIST_NAME = 'list_name'

    def get_lists(self):
        """Returns a list of Klaviyo lists"""
        return self._v2_request(self.LISTS, self.HTTP_GET)
    
    def create_list(self, list_name):
        """This will create a new list in Klaviyo.

        Args:
            list_name (str): A list name
        Returns:
            (dict) containing the list_id
        """
        data = {
            self.LIST_NAME: list_name
        }
        return self._v2_request(self.LISTS, self.HTTP_POST, data)

    def get_list_by_id(self, list_id):
        """This will fetch a list by its ID.

        Args:
            list_id (str): The the list id.
        Returns:
            (dict): information about the list
        """
        return self._v2_request('{}/{}'.format(self.LIST, list_id), self.HTTP_GET)
    
    def update_list_name_by_id(self, list_id, list_name):
        """This allows you to update a list's name.

        Args:
            list_id (str)
            list_name (str):

        Returns:
            empty str on success

        Raises:
            (KlaviyoApiException): Raised if request fails
        """
        params = {
            self.LIST_NAME: list_name
        }

        return self._v2_request('{}/{}'.format(self.LIST, list_id), self.HTTP_PUT, params)
        
    def delete_list(self, list_id):
        """Deletes a list by its ID

        Args:
            list_id (str): ID of the list to be deleted.

        Returns:
            empty str on success

        Raises:
            (KlaviyoApiException): Raised if request fails
        """
        return self._v2_request('{}/{}'.format(self.LIST, list_id), self.HTTP_DELETE)

    def add_subscribers_to_list(self, list_id, profiles):
        """Uses the subscribe endpoint to subscribe user to list, this obeys the list settings.

        Args:
            list_id (str): The list id.
            profiles (list of dict): List of dicts containing profile info.
                [{
                    'email': email_address,
                    // key:value profile properties
                }]

        Returns:
            (list of dicts): List of subscribed members or empty if double opt in is on
        """
        params = {
            self.PROFILES: profiles
        }
        return self._v2_request('{}/{}/{}'.format(self.LIST, list_id, self.SUBSCRIBE), self.HTTP_POST, params)

    def get_list_subscription_status(self, list_id, emails):
        """Check if profiles are on a list and not suppressed.

        Args:
            list_id (str): The list id.
            emails (list): A list of email addresses.

        Returns:
            (list) Profiles that are subscribed.
        """
        params = {
            self.EMAILS: emails
        }

        return self._v2_request('{}/{}/{}'.format(self.LIST, list_id, self.SUBSCRIBE), self.HTTP_GET, params)

    def delete_subscribers_from_list(self, list_id, emails):
        """Delete and remove profiles from list.

        Args:
            list_id (str): The list id
            emails (list): A list of email addresses

        Returns:
            Empty str if successful.
        """
        params = {
            self.EMAILS: emails
        }

        return self._v2_request('{}/{}/{}'.format(self.LIST, list_id, self.SUBSCRIBE), self.HTTP_DELETE, params)

    def add_members_to_list(self, list_id, profiles):
        """Adds a member to a list regardless of opt-in settings

        Args:
            list_id (str): The list id.
            profiles (list of dict): List of dicts containing profile info.
                [{
                    'email': email_address,
                    // key:value profile properties
                }]

        Returns:
            (list) of dicts containing the emails and profile id that were successful
        """
        params = {
            self.PROFILES: profiles
        }
        return self._v2_request('{}/{}/{}'.format(self.LIST, list_id, self.MEMBERS), self.HTTP_POST, params)

    def get_list_membership_status(self, list_id, emails):
        """Check if profiles are on a list.

        Args:
            list_id (str): The list id.
            emails (list): A list of email addresses.

        Returns:
            (list) of dicts corresponding to the email addresses on their list if they're on the list
        """
        params = {
            self.EMAILS: emails
        }

        return self._v2_request('{}/{}/{}'.format(self.LIST, list_id, self.MEMBERS), self.HTTP_GET, params)

    def delete_list_membership_status(self, list_id, emails):
        """Remove profiles from a list.

        Args:
            list_id (str): klaviyo list id
            emails (list): a list of email addresses

        Returns:
            Empty str if successful.
        """
        params = {
            self.EMAILS: emails
        }

        return self._v2_request('{}/{}/{}'.format(self.LIST, list_id, self.MEMBERS), self.HTTP_DELETE, params)

    def get_list_exclusions(self, list_id, marker=None):
        """Get all of the emails that have been excluded from a list along with the exclusion reason and exclusion time.

        Args:
            list_id (str):The list id.
            marker (int): Pagination mechanism offset.

        Returns:
            (list) of dicts containing an excluded email.
        """
        params = self._build_marker_param(marker)

        return self._v2_request('{}/{}/exclusions/{}'.format(self.LIST, list_id, self.ALL), self.HTTP_GET, params)

    def get_all_members(self, group_id, marker=None):
        """Get all of the emails in a given list or segment

        Args:
            group_id (str): The list id or the segment id.
            marker (int): Pagination mechanism offset.

        Returns:
            (list) of records containing profile IDs and emails and potentially a marker
        """
        params = self._build_marker_param(marker)

        return self._v2_request('group/{}/{}/{}'.format(group_id, self.MEMBERS, self.ALL), self.HTTP_GET, params)
