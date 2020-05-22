from .api_helper import KlaviyoAPI

STARTING_PAGE = 0
DEFAULT_BATCH_SIZE = 50
TIMELINE_BATCH_SIZE = DEFAULT_BATCH_SIZE + DEFAULT_BATCH_SIZE


class Metrics(KlaviyoAPI):
    EXPORT = 'export'
    METRIC_ID = 'metric_id'
    START_DATE = 'start_date'
    END_DATE = 'end_date'
    UNIT = 'unit'
    MEASUREMENT = 'measurement'
    BY = 'by'
    WHERE = 'where'

    def get_metrics(self, page=STARTING_PAGE, count=DEFAULT_BATCH_SIZE):
        """
        Args:
            page: int() page of results to return
            count: int() number of results to return
        Return:
            (dict): with data list of metrics
        """
        params = {
            self.PAGE: page,
            self.COUNT: count,
        }
        return self._v1_request(self.METRICS, self.HTTP_GET, params)
    
    def get_metrics_timeline(self, since=None, count=TIMELINE_BATCH_SIZE, sort=KlaviyoAPI.SORT_DESC):
        """"
        Fetches all of the metrics and its events regardless of the statistic
        Args:
            since (str or int): next attribute of the previous api call or unix timestamp
            count (int): number of events returned
            sort (str): sort order for timeline
        Returns:
            (dict): metric timeline information
        """
        params = {
            self.COUNT: count,
            self.SORT: sort,
            self.SINCE: since,
        }

        params = self._filter_params(params)
        url = '{}/{}'.format(self.METRICS, self.TIMELINE)

        return self._v1_request(url, self.HTTP_GET, params)
        
    def get_metric_timeline_by_id(self, metric_id, since=None, count=TIMELINE_BATCH_SIZE, sort=KlaviyoAPI.SORT_DESC):
        """"
        Returns a timeline of events for a specific metric
        Args:
            metric_id (str): metric ID for the statistic
            since (str or int): next attribute of the previous api call or unix timestamp
            count (int): number of events returned
            sort (str): sort order for timeline
        Returns:

        """
        params = {
            self.COUNT: count,
            self.SORT: sort,
            self.SINCE: since,
        }
        params = self._filter_params(params)
        url = '{}/{}/{}'.format(self.METRIC, metric_id, self.TIMELINE)

        return self._v1_request(url, self.HTTP_GET, params)

    def get_metric_export(
        self, 
        metric_id, 
        start_date=None, 
        end_date=None, 
        unit=None, 
        measurement=None, 
        where=None, 
        by=None, 
        count=None
        ):
        """
        Exports metric values (counts, uniques, totals)
        Args:
            metric_id:
            start_date:
            end_date:
            unit:
            measurement:
            where:
            by:
            count:
        Return:

        """
        params = {
            self.METRIC_ID: metric_id,
            self.START_DATE: start_date,
            self.END_DATE: end_date,
            self.UNIT: unit,
            self.MEASUREMENT: measurement,
            self.WHERE: where,
            self.BY: by,
            self.COUNT: count
        }
        params = self._filter_params(params)

        url = '{}/{}/{}'.format(self.METRIC, metric_id, self.EXPORT)

        return self._v1_request(url, self.HTTP_GET, params)