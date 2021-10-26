from awsutils.base.paginator import PaginatorBase
from awsutils.sqs.errors import SQSException
from awsutils.sqs.models.sqs_queue import SQSQueue
from awsutils.utils.pagination_config import PaginationConfig

class SQSListQueues(PaginatorBase):
    def __init__(self, client_handler) -> None:
        super(SQSListQueues, self).__init__(client_handler, 'list_queues')

    def paginate(self, queue_name_prefix = '', pagination_config = PaginationConfig()):
        try:
            response_iterator = self._iterator.paginate(
                QueueNamePrefix = queue_name_prefix,
                PaginationConfig = pagination_config.get_dict()
            )

            queue_list = []
            for response in response_iterator:
                for url in response['QueueUrls']:
                    queue = SQSQueue.from_url(
                        url,
                        self._client_handler
                    )
                    queue_list.append(queue)
            
            return queue_list
        except Exception as e:
            raise SQSException(str(e))
