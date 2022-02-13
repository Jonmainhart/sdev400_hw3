# sdev400_hw3
AWS API Gateway and Lambdas
## Introduction
This assignment demonstrates the successful creation of a REST API using Amazon API Gateway and connection to an Amazon Lambda backend to display the last 5 results of a specific sport and team entered by a user. The backend employs 3 DynamoDB tables to store and retrieve the scores. 
## DynamoDB Set Up
Before the API and Lambda are created, three DynamoDB tables (Hockey, Soccer, and Baseball) were created using AWS CLI to store the scores via the `makeSportsdb.sh` file and the JSON files containing the scores.
## AWS Lambda Concept of Operation
The Lambda function was created using the AWS Console and consists of two files: `lambda_function.py` and `dynamo_functions.py`. The lambda_function code accepts an event and passes information from the event to the supporting function then returns a message to the caller.
The `dynamo_functions.py` file contains functions which scan DynamoDB for tables with the names of the sport requested. If the table is found, the table is scanned for the team. If the table is not found, the user is alerted that they should look for one of the three available sports. If the team is found, the scores are retrieved from the table, sorted, and used to build a message which will be returned to the caller. 
The message parts are formatted to include the requested team name, the opposing team name, the scores, the result, and the game date. For example: Canadiens lost to Lightning 0 to 1 on 2021-07-07.

![Returned message format](/images/image004.png "Message format")
## API Concept of Operation
An API was created using the Amazon API Gateway. A GET method was created, the Method Request, Integration Request, and Method Response were set-up using the GET Method Execution view.

**The AWS account used to create this is no longer in service. Do not be alarmed by any identifiable information seen in the images.**
