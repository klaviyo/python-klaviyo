from .api_helper import KlaviyoAPI


class Segments(KlaviyoAPI):
    SEGMENTS = 'segments'
    MEMEBERS = 'members'

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
            self.EMAILS: emails
        }

        return self._v2_request()