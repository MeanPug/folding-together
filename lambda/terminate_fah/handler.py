#!/usr/bin/env python3
import boto3
import json
import os


def terminate_stack(stack_id):
    cloudformation = boto3.client('cloudformation')

    response = cloudformation.delete_stack(
        StackName=stack_id,
    )

    print(f'stack {stack_id} terminated')

    return True


def terminate_fah_solver(event, context):
    stack_id = terminate_stack(
        event['stack_id'],
    )

    return stack_id
