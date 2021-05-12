from .api_helper import KlaviyoAPI


class Campaigns(KlaviyoAPI):
    CAMPAIGNS = 'campaigns'
    CAMPAIGN = 'campaign'
    RECIPIENTS = 'recipients'

    def get_campaigns(self, page=None, count=None):
        """
        Returns a list of all the campaigns you've created.
        The campaigns are returned in reverse sorted order by
        the time they were created.

        https://apidocs.klaviyo.com/reference/campaigns#get-campaigns

        Args:
            page (str): For pagination, which page of results to return.
            count (str): For pagination, the number of results to return.
        """

        params = {
            self.PAGE: page,
            self.COUNT: count
        }

        return self._v1_request(self.CAMPAIGNS, self.HTTP_GET, params)

    def get_campaign_recipients(self, campaign_id, count=None, sort="asc"):
        """
        Returns summary information about email recipients for the campaign
        specified that includes each recipients email, customer ID, and status.

        https://apidocs.klaviyo.com/reference/campaigns#get-campaign-recipients

        campaign_id (str): The campaign id.
        count (str): For pagination, the number of results to return.
        sort (str): Sort order to apply to results, either ascending or descending.
         Valid values are asc or desc. Defaults to asc.

        """

        params = {
            self.COUNT: count,
            self.SORT: sort
        }

        return self._v1_request('{}/{}/{}'.format(self.CAMPAIGN, campaign_id, self.RECIPIENTS), self.HTTP_GET, params)
