#!/usr/bin/env python3
import boto3
import json
import os


def launch_stack(donor_name, donor_id, template_url=None, subnet_ids=None, vpc_id=None, key_name=None):
    cloudformation = boto3.client('cloudformation')

    response = cloudformation.create_stack(
        StackName=f'folding-together-solver-{donor_id}',
        TemplateURL=template_url,
        Parameters=[
            {
                'ParameterKey': 'KeyName',
                'ParameterValue': key_name,
            },
            {
                'ParameterKey': 'Subnets',
                'ParameterValue': subnet_ids,
            },
            {
                'ParameterKey': 'VpcId',
                'ParameterValue': vpc_id,
            },
            {
                'ParameterKey': 'FoldingAtHomeUser',
                'ParameterValue': donor_name
            }
        ],
        Capabilities=['CAPABILITY_IAM'],
        OnFailure='DELETE',
        Tags=[
            {
                'Key': 'Type',
                'Value': 'FAH Solver'
            },
        ]
    )

    print(f'generated stack {response["StackId"]}')

    return response['StackId']


def launch_fah_solver(event, context):
    print(f'got donor {event["donor_name"]} to launch fah stack')

    stack_id = launch_stack(
        event['donor_name'],
        event['donor_id'],
        template_url=os.getenv('TEMPLATE_URL'),
        subnet_ids=os.getenv('SUBNET_IDS'),
        vpc_id=os.getenv('VPC_ID'),
        key_name=os.getenv('KEY_NAME'),
    )

    return stack_id
