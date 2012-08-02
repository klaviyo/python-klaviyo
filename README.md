## What is Klaviyo?

Klaviyo is a real-time service for understanding your customers by aggregating all your customer data, identifying important groups of customers and then taking action.
http://www.klaviyo.com/

## What does this package do?

* Track customers and events directly from your backend.
* Track customers and events via JavaScript using a Django middleware.


## How to install?

    easy_install klaviyo

or

    pip install klaviyo


## Tracking events in Python

You can then easily use Klaviyo to track events or identify people:

    import klaviyo

    client = klaviyo.Klaviyo('YOUR_KLAVIYO_API_TOKEN')
    
    # Track an event...
    client.track('Filled out profile', email='someone@example.com', properties={
        'Added social accounts' : False,
    })

    # ...or just add a property to someone
    client.identify(email='someone@example.com', properties={
        'Plan' : 'Premium',
    })

Note that in these examples, I'm using `email` as the identifier. You can use `email` or your own ID or both. Here are some examples:

    import klaviyo

    client = klaviyo.Klaviyo('YOUR_KLAVIYO_API_TOKEN')
    
    # Track an event with ID
    client.track('Filled out profile', id=123)

    # Track an event with both ID and email
    client.track('Shared item', email='someone@example.com', id=123, properties={
        'Item type' : 'Photo',
    })

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