from enum import Enum
import gzip

CLRF = "\r\n"


class ResponseStatus(Enum):
    OK = "200 OK"
    CREATED = "201 Created"
    NOT_FOUND = "404 Not Found"
    METHOD_NOT_ALLOWED = "405 Method Not Allowed"

    def to_string(self) -> str:
        return self.value


class ContentType(Enum):
    TextPlain = "text/plain"
    ApplicationOctetStream = "application/octet-stream"

    def to_string(self) -> str:
        return self.value


class RequestType(Enum):
    Get = "GET"
    Post = "POST"

    def to_string(self) -> str:
        return self.value

    # @staticmethod
    # def from_string(request_type: str):
    #     return RequestType(request_type.upper())


def build_response(
    status: ResponseStatus,
    content_type: ContentType,
    headers: dict = {},
    body: str = "",
    version="1.1",
) -> bytes:
    resp_headers = {}
    resp_buff = bytearray()
    resp_buff.extend(f"HTTP/{version} {status.to_string()}{CLRF}".encode())

    if "connection" in headers.keys():
        resp_headers["Connection"] = headers["connection"]

    content = body.strip().encode()
    if "accept-encoding" in headers.keys():
        if "gzip" in headers["accept-encoding"]:
            content = gzip.compress(content)
            resp_headers["Content-Encoding"] = "gzip"

    if len(content) > 0:
        resp_headers["Content-Type"] = content_type.to_string()
        resp_headers["Content-Length"] = len(content)

    for key, value in resp_headers.items():
        resp_buff.extend(f"{key}: {value}{CLRF}".encode())

    resp_buff.extend(CLRF.encode())
    resp_buff.extend(content)

    return resp_buff
