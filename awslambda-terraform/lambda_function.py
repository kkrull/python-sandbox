import json


def lambda_handler(event, context):
    print('Hello from awslambda-terraform!')
    print('Event: {}'.format(json.dumps(event)))
    return {
        'body': {
            'event': event,
            'message': 'Hello from awslambda-terraform!',
        },
        'statusCode': 200,
    }
