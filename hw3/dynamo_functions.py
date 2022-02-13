"""
dynamo_functions.py

Jonathan Mainhart
SDEV 400
21 September 2021

dynamo functions for homework3.

Some of this code is courtesy of the examples provided by Amazon AWS team. Code snippets
are annotated throughout this file. Any snippets used are in compliance with the Apache
License, Version 2.0 as stipulated in the original work. A copy of the license is
available at https://aws.amazon.com/apache2.0

An example from Stack Overflow was used to help sort the returned list of dict objects.
The code is annotated below.
"""
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from operator import itemgetter

def table_exists(table_name):
    """
    Checks if a table exists with a given name.
    :param table_name: str
    :return: list of available tables
    
    # Use only in a clean DynamoDB as it will list all tables not just sports
    # might be weird to see Hockey, Baseball, BankingInfo, Soccer show up in your output
    
    Some portions of this code Copyright 2010-2019 
    Amazon.com, Inc. or its affiliates. All Rights Reserved.
    
    MoviesListTables.py
    """
    dynamodb = boto3.resource('dynamodb')
    
    tables_available = []
    for table in dynamodb.tables.all():
        tables_available.append(table.name) # Amazon
    return tables_available


def find_team(sport_name, team_name):
    """
    Scans a DynamoDB table for a specific team. Returns all scores if they exists,
    otherwise returns a formatted message specifying which teams are available to
    search for.
    :param sport_name: str
    :param team_name: str
    :return: list of dict objects if true, str if false
    """
    dynamodb = boto3.resource('dynamodb')
    result_set = dynamodb.Table(sport_name).scan(
           FilterExpression=Attr("HomeTeamName").eq(team_name) | Attr("AwayTeamName").eq(team_name) & Attr("GameDate").exists())
    for item in result_set["Items"]:
        if team_name in item["HomeTeamName"] or team_name in item["AwayTeamName"]:
            return result_set
    
    # the requested team is not in the table, get the available teams
    teams_available = dynamodb.Table(sport_name).scan(ProjectionExpression="HomeTeamName, AwayTeamName")
    
    # get rid of the duplicate names
    teams = []
    for team in teams_available["Items"]:
        if team["HomeTeamName"] not in teams:
            teams.append(team["HomeTeamName"])
        elif team["AwayTeamName"] not in teams:
            teams.append(team["AwayTeamName"])
            
    # return a formatted string containing the names
    return "{} not in {}. Try {}.".format(team_name, sport_name, ', '.join([str(team) for team in teams]))
    

def get_scores(sport_name, team_name):
    """
    Searches DynamoDB for specific sports and teams and returns a formatted message
    containing the last several scores if the team exists in the data set. The maximum
    number of scores is controlled by the MAX_SCORES constant.
    :param sport_name: str
    :param team_name: str
    :return: str
    """
    
    MAX_SCORES = 5
    
    dynamodb = boto3.resource('dynamodb')
    
    # sport and team name must be present
    if sport_name == '' or sport_name == None or team_name == '' or team_name == None:
        return "You must enter a sport and team name!"
    
    # check for sport
    sports_available = table_exists(sport_name)
    
    if sport_name not in sports_available:
        return ("{} not found. Try searching for {}".format(sport_name, sports_available))
    
    # get the scores - the scores may be a message
    scores = find_team(sport_name, team_name)
    
    
    formatted_scores = []
    score_template = '{} {} {} {} to {} on {}'
    
    # do the following if the scores are scores and not a message
    if type(scores) is not str:
        # sort the scores by GameDate - most recent on top
        # https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary#73050
        sorted_scores = sorted(scores["Items"], key=itemgetter('GameDate'), reverse=True) # thank you S.O.
        
        # get the latest n scores
        sorted_scores = sorted_scores[:MAX_SCORES]
        
        for item in sorted_scores:
            # assign values to variables
            home_team = item["HomeTeamName"]
            away_team = item["AwayTeamName"]
            home_score = item["HomeTeamScore"]
            away_score = item["AwayTeamScore"]
            game_date = item["GameDate"]
            
            # win - lose - tie conditions accounting for whether the requested team
            # is the home team or the away team - probably a cleaner way to handle this...
            if team_name == home_team and home_score > away_score:
                # requested team is home team - wins
                formatted_scores.append(score_template.format(home_team, 'beat', away_team, home_score, away_score, game_date))
            elif team_name == away_team and away_score > home_score:
                # requested team is away team - wins
                formatted_scores.append(score_template.format(away_team, 'beat', home_team, away_score, home_score, game_date))
            elif team_name == home_team and home_score < away_score:
                # requested team is home team - loses
                formatted_scores.append(score_template.format(home_team, 'lost to', away_team, home_score, away_score, game_date))
            elif team_name == away_team and away_score < home_score:
                # requested team is away team - loses
                formatted_scores.append(score_template.format(away_team, 'lost to', home_team, away_score, home_score, game_date))
            elif team_name == home_team and home_score == away_score:
                # requested team is home team - ties
                formatted_scores.append(score_template.format(home_team, 'tied', away_team, home_score, away_score, game_date))
            elif team_name == away_team and home_score == away_score:
                # requested team is away team - ties
                formatted_scores.append(score_template.format(away_team, 'tied', home_team, away_score, home_score, game_date))
        
        # create message  
        # this will make a string with newline separators which don't render - looks sloppy
        # tried using <br> but that didn't work either - looks as sloppy as \n
        # message = "The latest game results for {} {} are: {}".format(team_name, sport_name, '\n'.join([str(score) for score in formatted_scores]))
        
        # this will keep the list intact - looks better for this assignment
        message = "The latest game results for {} {} are: {}".format(team_name, sport_name, formatted_scores)
        
        # this returns the formatted scores message
        return message
        
    # otherwise return the message returned find_team()
    return scores
