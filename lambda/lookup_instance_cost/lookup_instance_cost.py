#!/usr/bin/env python3
import boto3


def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    stack_id = event.get("StackId", "none")
    if stack_id != "none":
        stack_id = stack_id['S']
        response = ec2_client.describe_tags(
            Filters=[
                {
                    'Name': 'resource-type',
                    'Values': ['instance']
                },
                {
                    'Name': 'tag:aws:cloudformation:stack-id',
                    'Values': [stack_id]
                },
            ],
            # should only return one since we are using one instance per donor
            # MaxResults=1
        )
        try:
            instance_id = response['Tags'][0]['ResourceId']
        except IndexError:
            return 0
        response = ec2_client.describe_spot_instance_requests(
            Filters=[
                {
                    'Name': 'instance-id',
                    'Values': [instance_id]
                },
            ]
        )
        return response['SpotInstanceRequests'][0]['ActualBlockHourlyPrice']
    else:
        return 0
