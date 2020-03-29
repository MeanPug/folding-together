#!/usr/bin/env python3
import boto3
import datetime
import json
import os


# Function for executing athena queries
def update_balance(amount, donor_id):
    cw_client = boto3.client('cloudwatch')
    metric_namespace = 'FT-Bank'
    metric_name = 'Balance'
    metric_dimension_name = 'Donor'
    # TODO protect against race conditions with reads and writes

    response = cw_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'currentValue',
                'MetricStat': {
                    'Metric': {
                        'Namespace': metric_namespace,
                        'MetricName': metric_name,
                        'Dimensions': [
                            {
                                'Name': metric_dimension_name,
                                'Value': donor_id
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    # 'Unit': 'Count'|'None'
                },
                # 'Expression': 'string',
                # 'Label': 'string',
                # 'ReturnData': True|False,
                # 'Period': 123
            },
        ],
        # Assume not processing more than one donation per donor per second
        StartTime=datetime.datetime.now() - datetime.timedelta(seconds=1),
        EndTime=datetime.datetime.now(),
        # NextToken='string',
        # ScanBy='TimestampDescending'|'TimestampAscending',
        # MaxDatapoints=123
    )
    new_value = 0
    if len(response['MetricDataResults'][0]['Values']) > 0:
        current_value = response['MetricDataResults'][0]['Values'][0]
        print(current_value)
        new_value = current_value + amount
    else:
        new_value = amount

    response = cw_client.put_metric_data(
        Namespace=metric_namespace,
        MetricData=[
            {
                'MetricName': metric_name,
                'Dimensions': [
                    {
                        'Name': metric_dimension_name,
                        'Value': donor_id
                    },
                ],
                'Timestamp': datetime.datetime.now(),
                'Value': new_value,
                # 'StatisticValues': {
                #     'SampleCount': 123.0,
                #     'Sum': 123.0,
                #     'Minimum': 123.0,
                #     'Maximum': 123.0
                # },
                # 'Values': [
                #     123.0,
                # ],
                # 'Counts': [
                #     123.0,
                # ],
                # 'Unit': 'Count'|'None',
                # 'StorageResolution': 123
            },
        ]
    )

    return new_value


def lambda_handler(event, context):
    sqs_client = boto3.client('sqs')
    response = sqs_client.receive_message(
        QueueUrl=os.environ['QueueUrl'],
        # AttributeNames=[
        #     'All'|'Policy'|'VisibilityTimeout'|'MaximumMessageSize'|'MessageRetentionPeriod'|'ApproximateNumberOfMessages'|'ApproximateNumberOfMessagesNotVisible'|'CreatedTimestamp'|'LastModifiedTimestamp'|'QueueArn'|'ApproximateNumberOfMessagesDelayed'|'DelaySeconds'|'ReceiveMessageWaitTimeSeconds'|'RedrivePolicy'|'FifoQueue'|'ContentBasedDeduplication'|'KmsMasterKeyId'|'KmsDataKeyReusePeriodSeconds',
        # ],
        # MessageAttributeNames=[
        #     'string',
        # ],
        MaxNumberOfMessages=1,  # TODO handle processing many messages
        VisibilityTimeout=5,  # TODO adjust as appropriate
        # WaitTimeSeconds=123,
        # ReceiveRequestAttemptId='string'
    )
    if "Messages" in response:
        # print('Found something!')
        # TODO handle processing many messages
        message = json.loads(response['Messages'][0]['Body'])
        # print(message['donation']['amount'])
        new_balance = update_balance(
            message['donation']['amount'],
            message['donor']['id'])
        # TODO delete messages from the queue when complete
        return 'New value is ' + str(new_balance) + ' cents.'
    else:
        return 'No messages'
