#!/usr/bin/env python3
import boto3
import os


# Function for executing athena queries
# def run_query(query, database, s3_output):
#     client = boto3.client('athena')
#     response = client.start_query_execution(
#         QueryString=query,
#         QueryExecutionContext={
#             'Database': database
#             },
#         ResultConfiguration={
#             'OutputLocation': s3_output,
#             }
#         )
#     print('Execution ID: ' + response['QueryExecutionId'])
#     return response


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
        MaxNumberOfMessages=1,
        VisibilityTimeout=60,
        # WaitTimeSeconds=123,
        # ReceiveRequestAttemptId='string'
    )
    print(response)
    return 'Success!'
