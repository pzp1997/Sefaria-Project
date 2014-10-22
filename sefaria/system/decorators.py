

from functools import wraps

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from sefaria.client.util import jsonResponse
import sefaria.system.exceptions as exps

import logging
logging.basicConfig()
logger = logging.getLogger("general")
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.ERROR)


def catch_error_as_json(func):
    """
    Decorator that catches InputErrors and translates them into JSON 'error' dicts for front end consumption.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except exps.InputError as e:
            return jsonResponse({"error": unicode(e)})
        return result
    return wrapper


def catch_error_as_http(func):
    """
    Decorator that catches InputErrors and returns an error page.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except exps.InputError as e:
            return render_to_response('static/generic.html',
                             {"content": u"There was an error processing your request: {}".format(str(e)) },
                             RequestContext(args[0]))
        return result
    return wrapper



def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Assumes that function doesn't change input data"""
        #logger.debug("Calling: " + func + "(" + args + kwargs + ")")
        result = func(*args, **kwargs)
        msg = func.__name__ + "(" + ",".join([str(a) for a in args])
        msg += ", " + str(kwargs) if kwargs else ""
        msg += "):\n\t" + str(result)
        logger.debug(msg)
        return result
    return wrapper