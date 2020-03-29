#!/usr/bin/env python3
import boto3
import json
import os


# Function for executing athena queries
def update_balance(amount, donor_id):
    ddb_client = boto3.client('dynamodb')
    response = ddb_client.update_item(
        TableName=os.environ['TableName'],
        Key={
            'Donor_id': {
                'S': donor_id,
            }
        },
        ReturnValues='ALL_NEW',
        ReturnConsumedCapacity='NONE',
        ReturnItemCollectionMetrics='NONE',
        UpdateExpression='ADD Balance :val',
        # ConditionExpression='string',
        ExpressionAttributeValues={
            ':val': {'N': str(amount)}
        }
    )

    return response['Attributes']['Balance']['N']


def lambda_handler(event, context):
    # print(event)
    for record in event['Records']:
        payload = json.loads(record['body'])
        # print(payload['donation']['amount'])
        donor_id_string = str(payload['donor']['id'])
        new_balance = update_balance(
            payload['donation']['amount'],
            donor_id_string)
        print('New value for ' + donor_id_string +
              ' is ' + str(new_balance) + ' cents.')
    return 'Success'
