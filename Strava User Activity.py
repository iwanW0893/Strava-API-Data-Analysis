# -*- coding: utf-8 -*-
"""
Spyder Editor

Sources:
    https://www.patricksteinert.de/wordpress/2017/11/29/analyzing-strava-training
    https://www.reddit.com/r/Strava/comments/bex8t4/strava_api_cannot_get_authorization_to_work/

"""

import os
import webbrowser
import stravalib
import json
import pandas as pd
import http.server

def credentials():
    client_id =  json.load(open(r'client.secret.txt')).get('Client ID')
    url =  json.load(open(r'client.secret.txt')).get('Access Token')
    client_secret =  json.load(open(r'client.secret.txt')).get('Client Secret')
    
    return client_id, url, client_secret
        
## requires clientid and full access in scope. copy and paste this

webbrowser.open(f'https://www.strava.com/oauth/authorize?scope=read,activity:read_all,profile:read_all,read_all&client_id={client_id}&response_type=code&redirect_uri=http://localhost:8888/strava-call-back.php&approval_prompt=force')

client_id, url, client_secret = credentials()

##no code yet, once authorized it has a code in it. copy this down

## example below. Replace the string with the code to populate the variable

code = "5d8b4a29ef1507454722ed3753c1c2a1ce3e6244"

## punch the code into client.exchange_code_for_token()
def api_access(code, client_id, client_secret):
    client = stravalib.client.Client() 
    token_response = client.exchange_code_for_token(client_id,client_secret,code)
    
    return client, token_response


def return_activities(client):
    activities = client.get_activities()
    my_cols= ['activity_id','name','distance', 'moving_time', 'elapsed_time', 'type', 'start_date_local', 'achievement_count','map']

    data = []

    for activity in activities:
        my_dict = activity.to_dict()
        my_dict['activity_id'] = my_dict.get('map').get('id').replace('a','')
        data.append(my_dict)
    df = pd.DataFrame(data,columns=my_cols)
    
    return df
    

def return_splits(df):
    for i, activity in df['activity_id'].iteritems():
        try:
            detail = client.get_activity(activity,include_all_efforts=True)
            splits = json.dumps(detail.to_dict().get('splits_metric'))
            df.at[i, 'splits_metric']= splits
        except:
            pass 
        
    return df
    
def output(df):
    df.to_csv(r'activities.csv')

    
    
client, token_response = api_access(code, client_id, client_secret)
df = return_activities(client)
df = return_splits(df)
printed = output(df)