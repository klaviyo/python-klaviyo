## CHANGELOG

### 3.0.1
- Python 2 compatible

### 3.0.0
- Redesign of the modules pattern.  Instead of using client.method_name we now utilize client.BASE_API_ENDPOINT.method_name
- For example in 2.* `client.get_metrics()` would now be `client.Metrics.get_metrics()` in 3.*
- There is no compatibility on migrating from 2.* to 3.* and will need to follow the new 3.0 pattern  


### 2.4
- As this changelog was craeted after 3.0, please refer to the README for version 2 https://github.com/klaviyo/python-klaviyo/tree/99be1d36941b2b48561575eda16e25224ce91367