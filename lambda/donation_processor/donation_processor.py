#!/usr/bin/env python3
import boto3
import json
import os


# Function for executing athena queries
def update_balance(amount, donor_id, donor_name):
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
        UpdateExpression='ADD Balance :val, SET Donor_Name=:name, SET StackId=empty',
        # ConditionExpression='string',
        ExpressionAttributeValues={
            ':val': {'N': str(amount)},
            ':name': {'S': str(donor_name)},
        }
    )

    return response['Attributes']['Balance']['N']


def lambda_handler(event, context):
    for record in event['Records']:
        payload = json.loads(record['body'])
        donor_info = payload['donor']

        new_balance = update_balance(
            payload['donation']['amount'],
            str(donor_info['id']),
            str(donor_info['name']),
        )

        print('New value for ' + str(donor_info['id']) + ' is ' + str(new_balance) + ' cents.')
    return 'Success'
