# -*- coding: UTF-8 -*-

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()
def get_current_user():
    try:
        return getattr( _thread_locals, 'user', None )
    except AttributeError:
        return 2 #sunyubin

def get_current_staffid():
    try:
        return get_current_user().get_profile().id
    except AttributeError:
        return 3 #sunyubin

def get_request():
    try:
        return _thread_locals.request
    except :
        return None

class ThreadLocals(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage.
    mrk: store request instead of user, because accessing user
         access session too so Vary: Cookie header is always added
    """

    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)