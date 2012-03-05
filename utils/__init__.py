import datetime

from functools import wraps
from django.http import HttpResponse
from django.utils import simplejson as json
from django.shortcuts import render_to_response
from django.template.context import RequestContext

START_DATE = datetime.datetime.now()
FIRST_MARKET_LOG = datetime.datetime.strptime('11.10.2010', '%d.%m.%Y')
TIME_SPEED = 2400

# Return fake current time
def current_time():
    now = datetime.datetime.now()
    diff = (now - START_DATE) * TIME_SPEED
    
    current = FIRST_MARKET_LOG + diff
    
    return current

# From: http://djangosnippets.org/snippets/821/
def render_to(template):
    """
    Decorator for Django views that sends returned dict to render_to_response function
    with given template and RequestContext as context instance.

    If view doesn't return dict then decorator simply returns output.
    Additionally view can return two-tuple, which must contain dict as first
    element and string with template name as second. This string will
    override template name, given as parameter

    Parameters:

     - template: template name to use
    """
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(template, output, RequestContext(request))
            return output
        return wrapper
    return renderer

# From: http://djangosnippets.org/snippets/2102/
def render_to_json(**jsonargs):
    """
    Renders a JSON response with a given returned instance. Assumes json.dumps() can
    handle the result. The default output uses an indent of 4.
    
    @render_to_json()
    def a_view(request, arg1, argN):
        ...
        return {'x': range(4)}

    @render_to_json(indent=2)
    def a_view2(request):
        ...
        return [1, 2, 3]

    """
    def outer(f):
        @wraps(f)
        def inner_json(request, *args, **kwargs):
            result = f(request, *args, **kwargs)
            r = HttpResponse(mimetype='application/json')
            if result:
                indent = jsonargs.pop('indent', 4)
                r.write(json.dumps(result, indent=indent, **jsonargs))
            else:
                r.write("{}")
            return r
        return inner_json
    return outer