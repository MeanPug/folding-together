#!/usr/bin/env python3
import boto3
# import os


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

    return 'Success!'
