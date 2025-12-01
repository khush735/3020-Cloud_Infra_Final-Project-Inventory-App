import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

# Helper function to convert Decimals to floats for JSON serialization
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, context):
    try:
        item_id = event['pathParameters']['id']
        location_id = int(event['queryStringParameters']['location_id'])
        
        # Check if item exists first
        response = table.get_item(
            Key={
                'item_id': item_id,
                'location_id': location_id
            }
        )
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Item not found'}, indent=2)
            }
        
        # Store the item data before deleting for the response
        deleted_item = response['Item']
        
        # Delete the item
        table.delete_item(
            Key={
                'item_id': item_id,
                'location_id': location_id
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Item deleted successfully',
                'deleted_item': deleted_item
            }, default=decimal_default, indent=2)
        }
    except KeyError as e:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': f'Missing required parameter: {str(e)}'}, indent=2)
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