from django.conf import settings

def is_trackable_response(request, response):
    return is_html_response(response) and not request.is_ajax()

def is_html_response(response):
    return 'text/html' in response.get('Content-Type', '')

def render_script(api_token):
        return """<script text="text/javascript">
  var _learnq = _learnq || [];
  _learnq.push(['account', '{}']);

  (function () {
    var b = document.createElement('script'); b.type = 'text/javascript'; b.async = true;
    b.src = ('https:' == document.location.protocol ? 'https://' : 'http://') + 'a.klaviyo.com/media/js/learnmarklet.js';
    var a = document.getElementsByTagName('script')[0]; a.parentNode.insertBefore(b, a);
  })();
</script>""".format(api_token)

class KlaviyoSnippetMiddleware(object):
    
    def process_response(self, request, response):
        try:
            api_token = settings.KLAVIYO_API_TOKEN
        except AttributeError:
            return response

        if is_trackable_response(request, response):
            insert_at = response.content.find('</body')
            if insert_at != -1:
                response.content = response.content[:insert_at] + \
                    render_script(api_token) + response.content[insert_at:]
                response['Content-Length'] = len(response.content)

        return response
