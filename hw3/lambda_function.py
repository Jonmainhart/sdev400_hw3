import json
import dynamo_functions

def lambda_handler(event, context):
    
    # call get_message() function to build the return message
    # TODO - DynamoDB tables are expecting a capitalized Sport and Team
    # unfortunaltely some team names have two capital letters
    # e.g. FC Montreal or Austin FC
    # so none of the built-in str methods will work for all cases.
    sport_name = event['SportName']
    team_name = event['TeamName']
    
    message = dynamo_functions.get_scores(sport_name, team_name)
    
    return {
        'statusCode': 200,
        'message': message
    }
