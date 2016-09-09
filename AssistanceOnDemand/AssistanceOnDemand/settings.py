"""
Django deployment settings for AssistanceOnDemand project.
"""

PRODUCTION = False


if PRODUCTION:
    try:
        from production_settings import *
    except ImportError:
        raise ImportError('The production_settings python file does not exist')
else:
    try:
        from development_settings import *
    except ImportError:
        raise ImportError('The dev_settings python file does not exist')