import json
import textwrap

class AWSObject:
    def __init__(self, client_handler, service_name) -> None:
        self._client = client_handler._client
        self._client_handler = client_handler
        self._service_name = service_name
        self.arn = None

    def __str__(self):
        NEWLINE = "\n"
        attrs = [
            f"{key} = {value}" 
            for key, value in vars(self).items() if not key.startswith('_')
        ]
        return_str = f"Type: {self.__class__.__name__}\n--------------------------\n"
        return_str += NEWLINE.join(attrs)

        return return_str