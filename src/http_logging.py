"""
HTTP logger hook (for dumping the request/response cycle).
"""
from contextlib import contextmanager
import json


###
# Logging state management
###

_enabled_stack = [False]
target = None


def push_state(enabled):
    _enabled_stack.append(enabled)


def pop_state():
    if len(_enabled_stack) == 1:
        # never pop the last state
        return bool(_enabled_stack[0])
    elif len(_enabled_stack) == 0:
        # something's gone terribly wrong
        raise RuntimeError("_enabled_stack should never be empty")
    else:
        return bool(_enabled_stack.pop())


def logging_enabled():
    return bool(_enabled_stack[-1])


@contextmanager
def temporarily_disabled():
    """Temporarily disable logging if it's enabled.

    with http_logging.temporarily_disabled():
        my_client.do_thing()

    """
    push_state(False)
    yield
    pop_state()


###
# Actual HTTP logging and hook
###

def _trim_headers(headers):
    sensitive_headers = [
        "X-VSS-PerfData",
        "X-TFS-Session",
        "X-VSS-E2EID",
        "X-VSS-Agent",
        "Authorization",
        "X-TFS-ProcessId",
        "X-VSS-UserData",
        "ActivityId",
        "P3P",
        "X-Powered-By",
        "Cookie",
    ]

    cleaned_headers = headers.copy()

    for sensitive_header in sensitive_headers:
        try:
            del cleaned_headers[sensitive_header]
        except KeyError:
            pass

    return dict(cleaned_headers)


def log_request(response, file):
    try:
        content = response.json()
    except ValueError:
        content = response.text

    data = {
        'request': {
            'url': response.request.url,
            'headers': _trim_headers(response.request.headers),
            'body': str(response.request.body),
            'method': response.request.method,
        },
        'response': {
            'headers': _trim_headers(response.headers),
            'body': content,
            'status': response.status_code,
            'url': response.url,
        },
    }

    json.dump(data, file, indent=4)


def requests_hook(response, *args, **kwargs):
    global target

    if logging_enabled() and target is not None:
        log_request(response, target)
