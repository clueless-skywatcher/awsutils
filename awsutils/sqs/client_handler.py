from awsutils.base.client_handler import ClientHandlerBase
from awsutils.sqs.errors import SQSException

class SQSQueueAttributes:
    def __init__(self,
        delay_seconds = "0",
        max_message_size = "262144",
        message_retention_period = "345600",
        receive_message_wait_time_seconds = "0",
        visibility_timeout = "0"
    ) -> None:
        self.delay_seconds = delay_seconds
        self.max_message_size = max_message_size
        self.message_retention_period = message_retention_period
        self.receive_message_wait_time_seconds = receive_message_wait_time_seconds
        self.visibility_timeout = visibility_timeout

    def get_dict(self):
        return {
            'DelaySeconds': self.delay_seconds,
            'MaximumMessageSize': self.max_message_size,
            'MessageRetentionPeriod': self.message_retention_period,
            'ReceiveMessageWaitTimeSeconds': self.receive_message_wait_time_seconds,
            'VisibilityTimeout': self.visibility_timeout
        }
        
class SQSClientHandler(ClientHandlerBase):
    def __init__(self, localstack = True, profile = None) -> None:
        super(SQSClientHandler, self).__init__('sqs', localstack = localstack, profile = profile)
        