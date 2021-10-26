class PaginatorBase:
    def __init__(self, client_handler, paginator) -> None:
        self._client_handler = client_handler
        self._client = client_handler._client
        self._iterator = self._client.get_paginator(paginator)

    def paginate(self, pagination_config):
        pass
