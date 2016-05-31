from functools import wraps

from django.http import HttpResponseRedirect
from oauth2client.contrib.django_orm import Storage

from gauth.models import CredentialsModel


def gauth_required(func):
    """
    Decorator that requires the user to authenticate
    with Google and authorize Sefaria to act on their behalf.
    If the user has already authenticated, it will call the wrapped function
    with the kwarg `credential` set to the obtained credentials.
    If not, it will start the OAuth 2.0 flow.
    At the moment, only used for sheets.views.export_to_drive.
    """
    @wraps(func)
    def inner(request, *args, **kwargs):
        storage = Storage(CredentialsModel, 'id', request.user, 'credential')
        credential = storage.get()

        if credential is None or credential.invalid:
            request.session['next_view'] = request.path
            return HttpResponseRedirect('/gauth')

        return func(request, credential, *args, **kwargs)
    return inner