from datetime import datetime as DateTime

from awsutils.base.model import AWSObject
from awsutils.sqs.errors import SQSException
from awsutils.sqs.models.sqs_message import SQSMessage
from awsutils.sqs.client_handler import SQSQueueAttributes

class SQSQueue(AWSObject):
    def __init__(self, client_handler, name, initializing = True, **kwargs):
        super(SQSQueue, self).__init__(client_handler, 'sqs')
        self.name = name
        self.arn = None
        self.approx_num_of_messages = None
        self.created_datetime = None
        self.delay = None
        self.last_modified = None
        self.visibility_timeout = None
        self.retention_period = None
        self.receive_message_wait_time = None
        self.max_message_size = None
        self._initializing = initializing
        self._non_existent = True
        self.url = None
        
        if not initializing:
            self._fetch_url()
            self._fetch_attributes()
            self._non_existent = False

    def _fetch_url(self):
        try:
            url_response = self._client.get_queue_url(
                QueueName = self.name
            )
            self.url = url_response.get('QueueUrl')
            self._non_existent = False
        except Exception as e:
            raise SQSException(str(e))

    @staticmethod
    def from_url(url, client_handler):
        try:
            queue = SQSQueue(
                client_handler,
                name = url.split('/')[-1],
                initializing = False
            )

            return queue
        except Exception as e:
            raise SQSException(f"Failed to create Queue with URL due to error: {str(e)}")

    def _fetch_attributes(self):
        try:
            attributes_response = self._client.get_queue_attributes(
                QueueUrl = self.url,
                AttributeNames = [
                    'All'
                ]
            )
            attributes_dict = attributes_response['Attributes']
            self.arn = attributes_dict['QueueArn']
            self.approx_num_of_messages = attributes_dict['ApproximateNumberOfMessages']
            self.created_datetime = DateTime.utcfromtimestamp(float(attributes_dict['CreatedTimestamp']))
            self.delay = attributes_dict['DelaySeconds']
            self.last_modified = DateTime.utcfromtimestamp(float(attributes_dict['LastModifiedTimestamp']))
            self.visibility_timeout = attributes_dict['VisibilityTimeout']
            self.retention_period = attributes_dict['MessageRetentionPeriod']
            self.receive_message_wait_time = attributes_dict['ReceiveMessageWaitTimeSeconds']
            self.max_message_size = attributes_dict['MaximumMessageSize']

        except Exception as e:
            raise SQSException(str(e))

    def _remove_attributes(self):
        self.arn = None
        self.approx_num_of_messages = None
        self.created_datetime = None
        self.delay = None
        self.last_modified = None
        self.visibility_timeout = None
        self.retention_period = None
        self.receive_message_wait_time = None
        self.max_message_size = None
        self.url = None
        self._non_existent = True

    def send_message(self, message: SQSMessage):
        try:
            self._client.send_message(
                QueueUrl = self.url,
                MessageBody = message.body
            )
        except Exception as e:
            raise SQSException(str(e))

    def receive_message(self, 
        message_attr_names = [],
        max_messages = 1,
        visibility_timeout = 0,
        wait_time_seconds = 0,
    ):
        try:
            response = self._client.receive_message(
                QueueUrl = self.url,
                AttributeNames = ['All'],
                MessageAttributeNames = message_attr_names,
                MaxNumberOfMessages = max_messages,
                VisibilityTimeout = visibility_timeout,
                WaitTimeSeconds = wait_time_seconds,
            )
            if 'Messages' not in response:
                raise SQSException('SQS queue failed to receive messages. Either there are no messages or you have to wait for the visibility timeout')

            messages_list = []
            for message in response['Messages']:                
                message_obj = SQSMessage(
                    self._client_handler,
                    message['Body'],
                    md5_of_body = message['MD5OfBody'],
                    approximate_receive_count = message['Attributes'].get('ApproximateReceiveCount', None),
                    sender_id = message['Attributes'].get('SenderId', None),
                    sent_timestamp = DateTime.utcfromtimestamp(
                        int(message['Attributes'].get('SentTimestamp', None)) // 1000
                    ),
                    sequence_no = message['Attributes'].get('SequenceNumber', None),
                    message_attrs = message.get('MessageAttributes', None)
                )  
                messages_list.append(message_obj)
            
            return messages_list
            
        except Exception as e:
            raise SQSException(str(e))

    def create_or_fetch(self, attrs = SQSQueueAttributes()):
        try:
            response = self._client.create_queue(
                QueueName = self.name,
                Attributes = attrs.get_dict()
            )
            if response.get('QueueUrl') is not None:
                self.url = response['QueueUrl']
                self._fetch_attributes()

        except self._client.exceptions.QueueNameExists:
            print(f"This queue already exists with the same name and different attribute(s). Fetching this queue...")
            self._fetch_url()
            self._fetch_attributes()
        except Exception as e:
            raise SQSException(str(e))

    def purge(self):
        try:
            self._client.purge_queue(
                QueueUrl = self.url
            )
        except Exception as e:
            raise SQSException(str(e))

    def delete(self):
        try:
            self._client.delete_queue(
                QueueUrl = self.url
            )
            self._remove_attributes()
        except Exception as e:
            raise SQSException(str(e))