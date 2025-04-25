from .pub_http import build_response, RequestType, ResponseStatus, ContentType


def handle_request(request_buffer: bytes):
    request_lines = request_buffer.decode("utf-8").splitlines()
    print(request_lines)
    request_type, request_path, request_version = request_lines[0].split()

    request_type = RequestType(request_type.upper())

    print(request_type.to_string(), request_path, request_version, sep="|")

    if request_type == RequestType.Get:
        if request_path == "/":
            return build_response(ResponseStatus.OK, ContentType.TextPlain)
        
        if request_path.startswith("/echo/"):
            content = request_path.replace("/echo/", "")
            return build_response(ResponseStatus.OK, ContentType.TextPlain, body=content)

    return build_response(ResponseStatus.NOT_FOUND, ContentType.TextPlain)
