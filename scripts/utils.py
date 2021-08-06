import os
# import sys
#
# import six

# if six.PY2:
#     pass
# else:
#     from urllib.parse import urlsplit


def get_setting(setting_name, default=None, convert=lambda _value: _value or None):
    value = os.getenv(setting_name)
    if not value:
        try:
            from dynaconf import settings

            value = settings.get(setting_name)
        except ImportError:
            pass

    value = value or default
    return convert(value)
