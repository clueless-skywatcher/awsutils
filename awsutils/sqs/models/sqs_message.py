from awsutils.base.model import AWSObject

class SQSMessage(AWSObject):
    def __init__(self, client_handler, body, **kwargs):
        super().__init__(client_handler, 'sqs')
        self.body = body
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    