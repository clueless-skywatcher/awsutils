from awsutils.sqs.client_handler import SQSClientHandler
from awsutils.sqs.models.sqs_message import SQSMessage
from awsutils.sqs.models.sqs_queue import SQSQueue
from awsutils.sqs.paginators import SQSListQueues

if __name__ == '__main__':
    client = SQSClientHandler(localstack = True, profile = 'localstack')
    # Create 2 queues
    queue = SQSQueue(client, 'EpsiQueue')
    queue.create_or_fetch()
    queue2 = SQSQueue(client, 'VilQueue')
    queue2.create_or_fetch()

    # Paginate the fetched queues
    paginator = SQSListQueues(client)
    queues = paginator.paginate()
    for q in queues:
        print(q)