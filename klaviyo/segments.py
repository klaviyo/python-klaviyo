from .api_helper import KlaviyoAPI


class Segments(KlaviyoAPI):
    SEGMENTS = 'segments'
    SEGMENT = 'segment'
    MEMBERS = 'members'
    ALL = 'all'

    def get_profiles_from_lists(self, segment_id, emails):
        """
        Checks if one or more emails are in a given segment.
        No distinction is made between a person not being in a given segment,
        and not being present in Klaviyo at all.
        Can check up to a maximum of 100 emails at a time.

        https://apidocs.klaviyo.com/reference/lists-segments#get-segment-members

        :param segment_id:
        :param emails:
        :return:
        """

        params = {
            self.EMAIL: emails
        }

        return self._v1_request('{}/{}/{}'.format(self.SEGMENT, segment_id, self.MEMBERS), self.HTTP_GET, params)

    def get_all_profiles(self, segment_id: str, marker: int = None):
        """
        Get all of the emails in a given segment.

        https://apidocs.klaviyo.com/reference/lists-segments#get-members

        Args:
            segment_id (str): The list id or the segment id.
            marker (int): Pagination mechanism offset.

        Returns:
            (list) of records containing profile IDs and emails and potentially a marker.
        """

        params = self._build_marker_param(marker)

        return self._v2_request('group/{}/{}/{}'.format(segment_id, self.MEMBERS, self.ALL), self.HTTP_GET, params)
