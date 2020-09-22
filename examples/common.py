from starlette.requests import Request


def get_client_ip(request: Request):
    """
    :param request:
    :return:
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]
    return request.client.host
