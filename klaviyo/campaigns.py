from .api_helper import KlaviyoAPI


class Campaigns(KlaviyoAPI):
    CAMPAIGNS = 'campaigns'
    CAMPAIGN = 'campaign'
    RECIPIENTS = 'recipients'

    OFFSET = 'offset'

    def get_campaigns(self, page=0, count=50):
        """Returns a list of all the campaigns you've created.
        The campaigns are returned in reverse sorted order by
        the time they were created.

        https://apidocs.klaviyo.com/reference/campaigns#get-campaigns

        Args:
            page (int): For pagination, which page of results to return.
            count (int): For pagination, the number of results to return.

        Returns:
            (list): containing the list of campaigns.
        """

        params = {
            self.PAGE: page,
            self.COUNT: count
        }

        return self._v1_request(self.CAMPAIGNS, self.HTTP_GET, params)

    def get_campaign_recipients(self, campaign_id, count=5000, offset='', sort="asc"):
        """Returns summary information about email recipients for the campaign
        specified that includes each recipients email, customer ID, and status.

        https://apidocs.klaviyo.com/reference/campaigns#get-campaign-recipients

        Args:
            campaign_id (str): The campaign id.
            count (int): For pagination, the number of results to return.
            offset (str): For pagination, the next_offset from the api response.
            sort (str): Sort order to apply to results, either ascending or descending.
             Valid values are asc or desc. Defaults to asc.
        Returns:
            (list): containing the campaign recipients.

        """

        params = {
            self.COUNT: count,
            self.SORT: sort,
            self.OFFSET: offset
        }

        return self._v1_request('{}/{}/{}'.format(self.CAMPAIGN, campaign_id, self.RECIPIENTS), self.HTTP_GET, params)
