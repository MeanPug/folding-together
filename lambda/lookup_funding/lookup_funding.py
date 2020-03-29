#!/usr/bin/env python3
import boto3
import os

minimum_funding_threshold_cents = 1


def lambda_handler(event, context):
    # print(event)
    ddb_client = boto3.client('dynamodb')
    response = ddb_client.scan(
        TableName=os.environ['TableName'],
        Select='ALL_ATTRIBUTES',
        ReturnConsumedCapacity='NONE',
        # TotalSegments=123,
        # Segment=123,
        # ProjectionExpression='string',
        FilterExpression='Balance >= :min',
        ExpressionAttributeValues={
            ':min': {'N': str(minimum_funding_threshold_cents)}
        },
        ConsistentRead=True
    )
    print(response)
    return 'Success'
