#!/usr/bin/env python3
import boto3
import datetime
import json
import os


metric_namespace = 'Bank'
metric_name = 'Balance'
metric_dimension_name = 'Cause'
metric_dimension_value = 'Any'
update_frequency_seconds = 60*60*4


# Function for executing athena queries
def update_balance(amount):
    cw_client = boto3.client('cloudwatch')
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
                                'Value': metric_dimension_value
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
        StartTime=datetime.datetime.now() - datetime.timedelta(
            seconds=update_frequency_seconds),
        EndTime=datetime.datetime.now(),
        # NextToken='string',
        # ScanBy='TimestampDescending'|'TimestampAscending',
        # MaxDatapoints=123
    )
    print(response)

    # response = cw_client.put_metric_data(
    #     Namespace='string',
    #     MetricData=[
    #         {
    #             'MetricName': 'string',
    #             'Dimensions': [
    #                 {
    #                     'Name': 'string',
    #                     'Value': 'string'
    #                 },
    #             ],
    #             'Timestamp': datetime(2015, 1, 1),
    #             'Value': 123.0,
    #             'StatisticValues': {
    #                 'SampleCount': 123.0,
    #                 'Sum': 123.0,
    #                 'Minimum': 123.0,
    #                 'Maximum': 123.0
    #             },
    #             'Values': [
    #                 123.0,
    #             ],
    #             'Counts': [
    #                 123.0,
    #             ],
    #             'Unit': 'Count'|'None',
    #             'StorageResolution': 123
    #         },
    #     ]
    # )


def lambda_handler(event, context):
    sqs_client = boto3.client('sqs')
    response = sqs_client.receive_message(
        QueueUrl=os.environ['QueueURL'],
        # AttributeNames=[
        #     'All'|'Policy'|'VisibilityTimeout'|'MaximumMessageSize'|'MessageRetentionPeriod'|'ApproximateNumberOfMessages'|'ApproximateNumberOfMessagesNotVisible'|'CreatedTimestamp'|'LastModifiedTimestamp'|'QueueArn'|'ApproximateNumberOfMessagesDelayed'|'DelaySeconds'|'ReceiveMessageWaitTimeSeconds'|'RedrivePolicy'|'FifoQueue'|'ContentBasedDeduplication'|'KmsMasterKeyId'|'KmsDataKeyReusePeriodSeconds',
        # ],
        # MessageAttributeNames=[
        #     'string',
        # ],
        MaxNumberOfMessages=1,  # TODO handle processing many messages
        VisibilityTimeout=5,
        # WaitTimeSeconds=123,
        # ReceiveRequestAttemptId='string'
    )
    if "Messages" in response:
        # print('Found something!')
        # TODO handle processing many messages
        message = json.loads(response['Messages'][0]['Body'])
        # print(message['donation']['amount'])
        update_balance(message['donation']['amount'])
    else:
        return 'No messages'
