try:
   from urllib.parse import urlencode
except ImportError:
   from urllib import urlencode

import base64
import json
import datetime
import time

import requests

KLAVIYO_API_SERVER = 'https://a.klaviyo.com/api'
KLAVIYO_DATA_VARIABLE = 'data'
PUBLIC_TOKEN_REQUESTS = ('identify', 'track')
TRACK_ONCE_KEY = '__track_once__'

TIMELINE = 'timeline'

CUD_REQUEST_TYPE = ("DELETE", "POST", "PUT")

class KlaviyoException(Exception):
    pass

class Klaviyo(object):
    
    def __init__(self, public_token=None, private_token=None, api_server=KLAVIYO_API_SERVER):
        self.public_token = public_token
        self.private_token = private_token
        self.api_server = api_server

        # if you only need to do one type of request, it's not required to have both private and public.. but we need at least 1 token
        if not self.public_token and not self.private_token:
            raise KlaviyoException('You must provide a public or private api token')

    def track(self, event, email=None, id=None, properties=None, customer_properties=None,
        timestamp=None, ip_address=None, is_test=False):
        
        if email is None and id is None:
            raise KlaviyoException('You must identify a user by email or ID.')
        
        if properties is None:
            properties = {}
        
        if customer_properties is None:
            customer_properties = {}
        
        if email: 
            customer_properties['email'] = email

        if id: 
            customer_properties['id'] = id

        params = {
            'token' : self.public_token,
            'event' : event,
            'properties' : properties,
            'customer_properties' : customer_properties,
            'time' : self._normalize_timestamp(timestamp),
        }

        if ip_address:
            params['ip'] = ip_address

        query_string = self._build_query_string(params, is_test)
        return self._request('track', query_string)
    
    def track_once(self, event, email=None, id=None, properties=None, customer_properties=None,
        timestamp=None, ip_address=None, is_test=False):
        
        if properties is None:
            properties = {}
        
        properties[TRACK_ONCE_KEY] = True
        
        return self.track(event, email=email, id=id, properties=properties, customer_properties=customer_properties,
            ip_address=ip_address, is_test=is_test)
    
    def identify(self, email=None, id=None, properties=None, is_test=False):
        if email is None and id is None:
            raise KlaviyoException('You must identify a user by email or ID.')
        
        if properties is None:
            properties = {}
        
        if email: properties['email'] = email
        if id: properties['id'] = id
        
        query_string = self._build_query_string({
            'token' : self.public_token,
            'properties' : properties,
        }, is_test)
        return self._request('identify', query_string)
    
    def metrics(self, page=0, count=50):
        """
        args:
            page: int() page of results to return
            count: int() number of results to return
        return:
            dict with data list of metrics
        """
        params = {
            'page': page,
            'count': count
        }
        metrics = self._request('metrics', params)
        return metrics
        
    def metric_timeline(self, metric_id=None, since=None, count=100, sort='desc'):
        """"
        args:
            since: str() or int() next attribute of the previous api call or unix timestamp
            count: int() number of events retuned
            sort: str() sort order for timeline
        """
        
        params = {
            'count': count,
            'sort': sort,
            'since': since
        }
        params = self._filter_params(params)
        
        if metric_id:
            url = '{}/{}/{}'.format('metric', metric_id, TIMELINE)
        else:
            url = '{}/{}'.format('metrics', TIMELINE)

        timeline = self._request(url, params)
        
        return timeline
    
    def metric_export(
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
        params = {
            'metric_id': metric_id,
            'start_date': start_date,
            'end_date': end_date, 
            'unit': unit,
            'measurement': measurement,
            'where': where,
            'by': by,
            'count': count
        }
        params = self._filter_params(params)
        
        url = '{}/{}/{}'.format(METRIC, metric_id, 'export')
        
        metric_export = self._request(url, params)
        
        return metric_export

    def lists(self, list_name=None, method='GET'):
        """
        args:
            method: str() optional type of request
            list_name: str() optional name of list to be created
        """
        api_version = 'v2'
        if method.upper() == 'GET':
            lists = self._request('lists', {}, api_version=api_version)
            return lists

        elif method.upper() == 'POST':
            params = {
                'list_name': list_name
            }
            created_list = self._request('lists', params, method=method, api_version=api_version)
            return created_list
        
    def list(self, list_id, list_name=None, method="GET",):
        """
        args:
            list_id: str() the list id
            list_name: str() name of the list - PUT to change it
        """
        if method == 'POST':
            raise KlaviyoException('The list endpoint only accepts GET, PUT, and DELETE methods')
        api_version = 'v2'
        params = {
            "list_name": list_name
        }
        params = self._filter_params(params)
        list_details = self._request('list/{}'.format(list_id), params, method=method, api_version=api_version)

        return list_details
        
    def list_subscription(self, list_id, data, subscription_type='subscribe', method="GET"):
        """
        args:
            list_id: str() the list id
            subscription_type: str() subscribe or members depending on the action
            data: for POST -> data must be a list of objects, for GET data must be a list of emails
            
        """
        api_version = 'v2'

        if method.upper() == "GET":
            if not isinstance(data, list) or not  all(isinstance(s, str) for s in data):
                raise KlaviyoException("Data must be a list of strings")

            params = {
                'emails': data
            }
            print(params)
            subscribed_members = self._request('list/{}/{}'.format(list_id, subscription_type), params, api_version=api_version)

        elif method.upper() == "POST":
            if not isinstance(data, list) or not isinstance(data[0], dict):
                raise KlaviyoException("Data must be a list of objects")

            params = {
                "profiles": data
            }
            subscribed_members = self._request('list/{}/{}'.format(list_id, subscription_type), params, method=method, api_version=api_version)

        return subscribed_members
    
    def unsubscribe_from_list(self, list_id, emails, subscription_type='subscribe'):
        """
        args:
            list_id: str() the list id
            subscription_type: str() subscribe or members depending on the action
            emails: a list of emails
        """
        api_version = 'v2'

        params = {
            'emails': emails
        }
        unsubscribed_emails = self._request('list/{}/subscribe'.format(list_id), params, method="DELETE", api_version=api_version)
        
        return unsubscribed_emails
    
    def list_exclusions(self, list_id, marker=None):
        """
        args:
            list_id: str() the list id
            marker: int() optional returned from the previous get call
        """
        api_version = 'v2'
        excluded_members = self._request('list/{}/exclusions/all', {}, api_version=api_version)

        return excluded_members
        
    def all_members(self, group_id, marker=None):
        """
        args:
            id: str() the list id or the segment id
            marker: int() optional returned from the previous get call
        """
        api_version = 'v2'
        all_members = self._request('group/{}/members/all'.format(group_id), {}, api_version=api_version)
        return all_members

    def _normalize_timestamp(self, timestamp):
        if isinstance(timestamp, datetime.datetime):
            timestamp = time.mktime(timestamp.timetuple())

        return timestamp

    def _build_query_string(self, params, is_test):
        return urlencode({
            KLAVIYO_DATA_VARIABLE : base64.b64encode(json.dumps(params).encode('utf-8')),
            'test' : 1 if is_test else 0,
        })
        
    def _filter_params(self, params):
        return dict((k,v) for k,v in params.items() if v is not None)


    def _request(self, path, params, method="GET", api_version=None):
        headers = {
            'Content-Type': "application/json",
        }
        if not api_version:
            api_version = 'v1'
        # to handle the track and identify requests
        if path in PUBLIC_TOKEN_REQUESTS:
            if not self.public_token:
                raise KlaviyoException('Public token is not defined')

            url = '{}/{}?{}'.format(self.api_server, path, params)
            response = getattr(requests, method.lower())(url, headers=headers)

            return response.text == '1'
        
        # this is to handle all the private api requests
        else:
            if not self.private_token:
                raise KlaviyoException('Private token is not defined')

            if method.upper() == "GET":
                params.update({
                    "api_key": self.private_token
                })

                if api_version == 'v2':
                    params = json.dumps(params)
                    
                    url = '{}/{}/{}'.format(
                        self.api_server, 
                        api_version, 
                        path, 
                    )
                    response = getattr(requests, method.lower())(url, headers=headers, data=params)

                else:
                    params = urlencode(params)
                    url = '{}/{}/{}?{}'.format(
                        self.api_server, 
                        api_version, 
                        path, 
                        params
                    )
                    
                    response = getattr(requests, method.lower())(url, headers=headers)

                return response.json()
                
            elif method.upper() in CUD_REQUEST_TYPE:
                url = '{}/{}/{}'.format(
                    self.api_server,
                    api_version,
                    path
                )
                params.update({
                    "api_key": self.private_token
                })
                if api_version == 'v2':
                    params = json.dumps(params)

                response = getattr(requests, method.lower())(url, headers=headers, data=params)
                
                # some successful posts/puts/deletes don't return json and return empty str, so let's return a 1 showing success as errors will always be json
                try:
                    return response.json()
                except ValueError:
                    return '1'
