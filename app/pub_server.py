import os
from .pub_http import build_response, RequestType, ResponseStatus, ContentType


def handle_request(request_buffer: bytes):
    base_dir = os.getenv("BASE_DIR")
    request_lines = request_buffer.decode("utf-8").splitlines()
    print(request_lines)
    request_type, request_path, request_version = request_lines[0].split()
    request_type = RequestType(request_type.upper())
    request_version = request_version.split("/")[-1]

    request_headers = {}
    index = 1
    for line in request_lines[1:]:
        if line.find(": ") == -1:
            break
        key, value = line.split(": ", 1)
        request_headers[key.lower()] = value.strip()
        index += 1

    request_body = bytes()
    if index < len(request_lines):
        request_body = "\n".join(request_lines[index:]).strip().encode()

    print(request_type.to_string(), request_path, request_version, sep="|")

    if request_type == RequestType.GET:
        if request_path == "/":
            return build_response(
                ResponseStatus.OK,
                ContentType.TextPlain,
                headers=request_headers,
                version=request_version,
            )

        if request_path.startswith("/echo/"):
            content = request_path.replace("/echo/", "").encode()
            return build_response(
                ResponseStatus.OK,
                ContentType.TextPlain,
                body=content,
                headers=request_headers,
                version=request_version,
            )

        if request_path == "/user-agent":
            content = request_headers.get("user-agent").encode()
            return build_response(
                ResponseStatus.OK,
                ContentType.TextPlain,
                body=content,
                headers=request_headers,
                version=request_version,
            )

        if request_path.startswith("/files/"):
            filename = request_path[7:]
            file_path = os.path.join(base_dir, filename)
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    content = f.read()
                    return build_response(
                        ResponseStatus.OK,
                        ContentType.ApplicationOctetStream,
                        body=content,
                        headers=request_headers,
                        version=request_version,
                    )
            else:
                return build_response(
                    ResponseStatus.NOT_FOUND,
                    ContentType.TextPlain,
                    version=request_version,
                )

        return build_response(
            ResponseStatus.NOT_FOUND,
            ContentType.TextPlain,
            version=request_version,
        )

    if request_type == RequestType.POST:
        if request_path.startswith("/files/"):
            filename = request_path[7:]
            file_path = os.path.join(base_dir, filename)
            with open(file_path, "wb") as f:
                f.write(request_body)
                return build_response(
                    ResponseStatus.CREATED,
                    ContentType.ApplicationOctetStream,
                    headers=request_headers,
                    version=request_version,
                )

        return build_response(
            ResponseStatus.NOT_FOUND,
            ContentType.TextPlain,
            version=request_version,
        )

    return build_response(
        ResponseStatus.METHOD_NOT_ALLOWED,
        ContentType.TextPlain,
        version=request_version,
    )
