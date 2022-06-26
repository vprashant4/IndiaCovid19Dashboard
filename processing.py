# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 23:16:18 2022

@author: Happy
"""
#importing pandas package
import pandas as pd

#opening json file
data = pd.read_json('mohfw.json')
#normalization data
covid_data = pd.json_normalize(data['rows'])
#drop un-useful columns
covid_data.drop(columns = ["id", "key", "value._id", 
                           "value._rev", "value.confirmed_india",
                           "value.confirmed_foreign", "value.source"], 
                inplace=True)
#rename colomus names
covid_data.rename(columns = {'value.report_time':'report_time', 
                             'value.state':'states_abbreviations',
                              'value.cured':'cured',
                              'value.death':'death',
                              'value.type':'type',
                              'value.confirmed':'confirmed'}, inplace = True)
#manipulating data and time and seconds
covid_data['date_created'] = pd.to_datetime(covid_data['report_time'], errors='coerce')
covid_data['Date'] = covid_data['date_created'].dt.strftime("%Y-%m-%d")
covid_data['Time'] = covid_data['date_created'].dt.strftime("%H:%M:%S")
covid_data.drop(columns = ["date_created"], inplace=True)

#opening states abbreviations csv file
states_df = pd.read_csv('states_abbreviations.csv', sep=',')
#merging covid dataframe to states abbreviations dataframe
covid_data=pd.merge(covid_data, states_df, on ='states_abbreviations')
#exporting merge covid data into csv file
covid_data.to_csv('covid19_india_clearned.csv', index = False)
