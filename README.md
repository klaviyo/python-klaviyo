# python-klaviyo - DEPRECATED

# Deprecation Notice

This SDK and its associated pip package are set to be deprecated on April 1st 2023 and will not receive further updates.

We recommend migrating over to our [newest SDK](https://github.com/klaviyo/klaviyo-api-python).

You can read more about our SDK release history and support [here](https://developers.klaviyo.com/en/docs/sdk_overview)

For a comparison between our old and new APIs, check out [this guide](https://developers.klaviyo.com/en/docs/apis_comparison_chart).


# What is Klaviyo?

Klaviyo is a real-time service for understanding your customers by aggregating all your customer data, identifying important groups of customers and then taking action.
http://www.klaviyo.com/

## What does this package do?

* Track customers and events directly from your backend.
* Track customers and events via JavaScript using a Django middleware.


## How to install?

    easy_install klaviyo

or

    pip install klaviyo

## Response Object

All of the methods will return a KlaviyoAPIResponse object containing two attributes status_code and data.  
For example, if you wanted to create a list you would do the following:

    response = client.Lists.create_list(list_name)
    response.data # returns information about the created list
    response.status_code # returns the http status code of the response


## API Examples

After installing the klaviyo package you can initiate it using your public token which is for track events or identifying profiles and/or your private api key to utilize the metrics and list apis.

    import klaviyo

    client = klaviyo.Klaviyo(public_token=PUBLIC_TOKEN, private_token=PRIVATE_TOKEN)

You can then easily use Klaviyo to track events or identify people.  Note, track and identify requests take your public token.

    # Track an event...
    client.Public.track('Filled out profile', email='someone@mailinator.com', properties={
        'Added social accounts' : False,
    })
    
    # you can also add profile properties
    client.Public.track(
      'Filled out profile', 
      email='someone@mailinator.com', 
      properties={
        'Added social accounts' : False,
      }, 
      customer_properties={
        '$first_name': 'Thomas',
        '$last_name': 'Jefferson'
      }
    )

    # ...or just add a property to someone
    client.Public.identify(email='thomas.jefferson@mailinator.com', properties={
        '$first_name': 'Thomas',
        '$last_name': 'Jefferson',
        'Plan' : 'Premium',
    })

You can get metrics, a timeline of events and export analytics for a metric.  See here for more https://www.klaviyo.com/docs/api/metrics

    # return all metrics
    client.Metrics.get_metrics()
      args/kwargs:
        page=0
        count=50
    
    # return a timeline of all metrics
    client.Metrics.get_metrics_timeline()
      args/kwargs:
        since=None (unix or returned uuid from request)
        count=100
        sort='desc'

    # you can query for a specific metric id
    client.Metrics.get_metric_timeline_by_id(metric_id)
      args/kwargs:
        since=None (unix or returned uuid)
        count=50
        sort='desc'
    
    Export metric specific values
    client.Metrics.get_metric_export(metric_id)
      args/kwargs:
        start_date
        end_date
        unit
        measurement
        where 
        by
        count

You can create, update, read, and delete lists.  See here for more information https://www.klaviyo.com/docs/api/v2/lists

    # to get all lists
    client.Lists.get_lists()
    
    # to add a new list
    client.Lists.create_list(list_name)
    
    # get list details
    client.Lists.get_list_by_id(list_id)
    
    # update list name
    client.Lists.update_list_name_by_id(
      list_id, 
      list_name='NEW_LIST_NAME',
    )
    
    # delete a list
    client.Lists.delete_list(list_id)
    
    # Add subscribers to a list, this will follow the lists double opt in settings
    client.Lists.add_subscribers_to_list(list_id, profiles)
        profiles: is list of objects formatted like {'email': EMAIL, 'custom_property': NAME}
     
    # Check email address subscription status to a list
    client.Lists.get_subscribers_from_list(list_id, emails)
        emails: is a list of email addresses
    
    # Unsubscribe and remove profile from a list
    client.Lists.delete_subscribers_from_list(list_id, emails)
        emails: is a list of email addresses 

    # Add members to a list, this doesn't care about the list double opt in setting
    client.Lists.add_members_to_list(list_id, profiles)
        profiles: is list of objects formatted like {'email': EMAIL, 'custom_property': NAME}
        
    # Check email addresses if they're in a list
    client.Lists.get_members_from_list(list_id_, emails)
        emails: is a list of email addresses
     
    # Remove emails from a list
    client.Lists.remove_members_from_list(list_id, emails)
        emails:  a list of email addresses
    
    # get exclusion emails from a list - marker is used for paginating
    client.Lists.get_list_exclusions(list_id, marker=None)
    
    # get all members in a group or list
    client.Lists.get_all_members(group_id, marker=None)

    # check if email is in a segment, takes a list of emails.
    client.Lists.get_members_from_segment(segment_id, [emails])
    
You can fetch profile information given the profile ID. See here for more information: https://www.klaviyo.com/docs/api/people

    # get profile by profile_id
    client.Profiles.get_profile(profile_id)
    
    # update a profile
    client.Profiles.update_profile(profile_id, properties) # properties is a dict

    # unset properties on a profile
    client.Profiles.unset_profile_properties(
        profile_id,
        properties=['snake_case_property', 'camelCaseProperty', 'This one has spaces']
    )
    
    # get all metrics for a profile with the default kwargs
    # to paginate the responses you will get a UUID returned from the response, see here for more information
    # https://www.klaviyo.com/docs/api/people#metrics-timeline
    client.Profiles.get_profile_metrics_timeline(profile_id, since=None, count=100, sort='desc')

    # get all events of a metric for a profile
    # to paginate the responses you will get a UUID returned from the response
    # https://www.klaviyo.com/docs/api/people#metric-timeline
    client.Profiles.get_profile_metrics_timeline_by_id(profile_id, metric_id, since=None, count=100, sort='desc')

You can fetch the profile ID for a given email:

    # get the profile_id for 'thomas.jefferson@mailinator.com'
    client.Profiles.get_profile_id_by_email('thomas.jefferson@mailinator.com')

You can request profile deletion based on an email, phone number, or profile ID. See here for more information: https://www.klaviyo.com/docs/api/v2/data-privacy

    # request deletion of the profile tied to 'thomas.jefferson@mailinator.com'
    client.DataPrivacy.request_profile_deletion(identifier='thomas.jefferson@mailinator.com, id_type='email')

You can fetch information from campaigns:

    # request all campaigns
    client.Campaigns.get_campaigns(page=0, count=50)
    
    # get campaign recipients (offset can be found from the next_offset in the previous response)
    client.Campaigns.get_campaign_recipients(campaign_id, count=5000, offset='', sort='asc')

## Rate Limiting
  If a rate limit happens it will throw a klaviyo.exceptions.KlaviyoRateLimitException
  This will contain a detail key with a string value mentioning the time to back off in seconds

## How to use it with a Django application?

To automatically insert the Klaviyo script in your Django app, you need to make a few changes to your settings.py file. First,
add the following setting:

    KLAVIYO_API_TOKEN = 'YOUR_KLAVIYO_API_TOKEN'

then add the Klaviyo middleware at the top of the `MIDDLEWARE_CLASSES`:

    MIDDLEWARE_CLASSES = [
        'klaviyo.middleware.KlaviyoSnippetMiddleware',
        # Other classes
    ]

This will automatically insert the Klaviyo script at the bottom on your HTML page, right before the closing `body` tag.
