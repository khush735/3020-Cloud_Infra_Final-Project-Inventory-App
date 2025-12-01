import json
import boto3
import uuid
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    try:
        # Parse the JSON body from the request
        body = json.loads(event['body'])
        
        # Generate a unique ID using uuid (no external dependencies needed)
        new_item_id = str(uuid.uuid4())
        
        item = {
            'item_id': new_item_id,
            'item_name': body['item_name'],
            'item_description': body['item_description'],
            'item_qty_on_hand': int(body['item_qty_on_hand']),
            'item_price': Decimal(str(body['item_price'])),  # Convert to Decimal
            'location_id': int(body['location_id'])
        }
        
        table.put_item(Item=item)
        
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Item added successfully', 
                'item_id': new_item_id,
                'item_data': item
            }, default=str, indent=2)  # Use default=str to handle Decimal
        }
    except KeyError as e:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': f'Missing required field: {str(e)}'}, indent=2)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)}, indent=2)
        }