#!/usr/bin/python3

import urllib

def web_socket_do_extra_handshake(request):
    url_parts = urllib.parse.urlsplit(request.uri)
    request.extra_headers.append(('Set-Cookie', 'ws_test_'+(url_parts.query or '')+'=test; Path=/; HttpOnly\x0D\x0ASec-WebSocket-Origin: '+request.ws_origin))

def web_socket_transfer_data(request):
    # Expect close from user agent.
    request.ws_stream.receive_message()
