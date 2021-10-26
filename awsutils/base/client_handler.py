import boto3
from botocore.exceptions import ClientError

LOCALSTACK_ENDPOINT = 'http://localhost:4566'

class ClientHandlerBase:
    def __init__(self, 
        service_name,
        localstack = True,
        aws_access_key_id = None, 
        aws_secret_key = None,
        region = None,
        profile = None
    ) -> None:
        self._service_name = service_name
        if localstack:
            if profile is not None:
                session = boto3.Session(
                    aws_access_key_id = aws_access_key_id,
                    aws_secret_access_key = aws_secret_key,
                    region_name = region,
                    profile_name = profile
                )

                self._client = session.client(
                    service_name, 
                    endpoint_url = LOCALSTACK_ENDPOINT
                )
            else: 
                self._client = boto3.client(
                    service_name,
                    aws_access_key_id = aws_access_key_id,
                    aws_secret_access_key = aws_secret_key,
                    region_name = region,
                    endpoint_url = LOCALSTACK_ENDPOINT
                )
        else:
            if profile is not None:
                session = boto3.Session(
                    aws_access_key_id = aws_access_key_id,
                    aws_secret_access_key = aws_secret_key,
                    region_name = region,
                    profile_name = profile
                )

                self._client = session.client(
                    service_name
                )
            else: 
                self._client = boto3.client(
                    service_name,
                    aws_access_key_id = aws_access_key_id,
                    aws_secret_access_key = aws_secret_key,
                    region_name = region,
                )