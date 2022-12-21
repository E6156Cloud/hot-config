from flask import Flask
import boto3
import logging
from boto3.dynamodb.conditions import Key, Attr

application = Flask(__name__)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_USER = "user_configs"
REGION = "us-east-1"
HARDWARE_CATEGORIES = ['CPU', 'GPU', 'RAM', 'SSD', 'HDD', 'USB']

@application.route('/')
def handler():
    # db = boto3.client('dynamodb')
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    table = dynamodb.Table(TABLE_USER)

    details = []
    for cat in HARDWARE_CATEGORIES:
        response = table.query(
            IndexName='category-count-index',
            KeyConditionExpression=Key('category').eq(cat), ScanIndexForward=False)
        # print(response)
        try:
            details.append(response['Items'][0]['model'])
            logger.info(response)
        except:
            details.append('no model found for {}'.format(cat))
            logger.info(response['Items'][0])
            logger.info("fail to load config for {}".format(cat))
    # print(details)
    res = dict(zip(HARDWARE_CATEGORIES, details))
    # print(res)
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        'body': res
    }


if __name__ == '__main__':
    application.run()
