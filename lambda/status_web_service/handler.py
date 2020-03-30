import json
import boto3
import os


def get_canonical_status(stack_id, balance):
    """ the canonical status is a function of whether a stack has been spun up and the current balance on the account """
    if not stack_id:
        return 'QUEUED'
    elif stack_id and balance > 100:
        return 'PROCESSING'
    else:
        return 'FINISHED'


def donation_status(event, context):
    ddb_client = boto3.client('dynamodb')

    donation_id = event['pathParameters']['id']
    response = ddb_client.scan(
        TableName=os.getenv('TABLE_NAME'),
        Select='ALL_ATTRIBUTES',
        ReturnConsumedCapacity='NONE',
        FilterExpression='Donor_id = :donation',
        ExpressionAttributeValues={
            ':donation': {'S': donation_id}
        },
        ConsistentRead=True
    )

    try:
        donation = response['Items'][0]
    except IndexError:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': f'no donation with ID {donation_id} exists'})
        }

    body = {
        'data': {
            'canonical_status': get_canonical_status(donation['StackId']['S'], int(donation['Balance']['N'])),
            'balance_remaining': int(donation['Balance']['N'])
        }
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
