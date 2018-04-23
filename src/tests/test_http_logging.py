from argparse import Namespace
import io

import http_logging


def test_logging():
    f = io.StringIO()

    response = Namespace(
        request = Namespace(
            url = 'https://example.com/fake',
            headers = {
                'X-Request-Test-Header': 'keep',
                'Authorization': 'filter-out',
            },
            body = '',
            method = 'GET'
        ),
        headers = {
                'X-Response-Test-Header': 'keep',
                'Cookie': 'filter-out',
            },
        status_code = 200,
        url = 'https://example.com/fake/response',
        json = lambda: ""
    )

    http_logging.log_request(response, f)

    f.seek(0)
    contents = f.read()

    # ensure we don't strip arbitrary headers
    assert 'X-Request-Test-Header' in contents
    assert 'X-Response-Test-Header' in contents

    # ensure we strip sensitive headers
    assert 'Authorization' not in contents
    assert 'Cookie' not in contents
