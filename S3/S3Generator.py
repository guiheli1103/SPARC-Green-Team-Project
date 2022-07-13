import json
import boto3
import botocore
import logging
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    # intent name
    intent_name = event['interpretations'][0]['intent']['name']

    slots = event['interpretations'][0]['intent']['slots']
    # bucket name
    bucket_name = slots['BucketName']['value']['interpretedValue']

    # region name
    region_name = slots['RegionName']['value']['interpretedValue']

    # event here is key: value dictionary
    print('Your bucketname is ' + str(bucket_name))
    print('Your regionname is ' + str(region_name))

    # defaul response assume request is fullfilled
    response = {
        'sessionState': {
            'dialogAction': {
                'type': 'Close'
            },
            'intent': {
                'name': intent_name,
                'state': 'Fulfilled'
            }
        },
        'messages': [
            {
                'contentType': 'PlainText',
                'content': 'None'
            }
        ]
    }

    response_message = ''
    intent_state = 'Fulfilled'
    if create_bucket(bucket_name, region_name):
        response_message = 'bucket ' + bucket_name + \
            ' created at region' + region_name + 'successfully'
        response['messages'][0]['content'] = response_message
    else:
        response_message = 'Failed to create bucket ' + bucket_name
        intent_state = 'Failed'
    response['messages'][0]['content'] = response_message
    response['sessionState']['intent']['state'] = intent_state

    return response


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    print('bucket namae in create_bucket func is' + str(bucket_name))
    print('region name in create_bucket func is ' + str(region))
    try:
        if region is None or region == 'us-east-1':
            print("region is None")
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            print("regsion is " + str(region))
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)

    except ClientError as e:
        logging.error(e)
        print(e)
        return False

    return True
