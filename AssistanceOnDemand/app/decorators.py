from functools import wraps
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

def loginRequired(function):
    """
    Check if the user is connected
    Decorator for function-based  views 
    """
    def wrap(request, *args, **kwargs):
        if 'id' not in request.session.keys() and 'username' not in request.session.keys():
            return redirect('/login/')
        return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap

def loginRequiredView(View): 
    """
    Check if the user is connected
    Decorator for class-based views 
    """
    View.dispatch = method_decorator(loginRequired)(View.dispatch)
    return View