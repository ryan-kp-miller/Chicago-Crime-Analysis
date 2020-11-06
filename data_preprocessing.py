#!/usr/bin/env python
# coding: utf-8

# Data Preprocessing

# Reading in the Original Datasets and Combining Them

import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta

import warnings
warnings.filterwarnings('ignore')

crimes_general = pd.read_csv("Data/crimes_general.csv", parse_dates=['Date'])
crimes_murders = pd.read_csv("Data/crimes_murders.csv", parse_dates=['Date'])

#combining general crimes and homicides
crimes = pd.concat([crimes_general, crimes_murders], ignore_index=True)

#converting arrest column from boolean to int
crimes['Arrest'] = crimes['Arrest'].astype(int)


# Reducing the Number of Crimes

#filter for crimes between 2010-2019
crimes_cleaned = crimes[(crimes.Year >= 2010) & (crimes.Year <= 2019)].copy()


# Removing Unneeded Columns

#creating a list of the columns to drop
drop_cols = ['ID','Case Number', 'Block', 'Description', 
             'Beat', 'District', 'Ward', 'IUCR', 'FBI Code', 
             'Location', 'X Coordinate', 'Y Coordinate', 
             'Updated On']

#dropping the columns
crimes_cleaned.drop(labels=drop_cols, axis=1, inplace=True)


# Cleaning Up Text Columns

# Primary Type

#list of other values to group under "NON-CRIMINAL"
non_criminal_list = ['NON - CRIMINAL','NON-CRIMINAL (SUBJECT SPECIFIED)']

#replacing the other values with "NON-CRIMINAL"
crimes_cleaned['Primary Type'].replace(to_replace = non_criminal_list,
                                       value='NON-CRIMINAL', regex=False,
                                       inplace=True)

#Converting values to title case
crimes_cleaned['Primary Type'] = crimes_cleaned['Primary Type'].str.title()


# Location Description

#reading in manual mapping of unique original values to new ones
location = pd.read_csv('Data/Location.csv')

#merging the crimes_cleaned df with the location df
crimes_cleaned = crimes_cleaned.merge(location, how='left',
                                      left_on='Location Description',
                                      right_on='Original Value')

#removing the original value columns
crimes_cleaned.drop(labels=['Location Description','Original Value'],axis=1,
                    inplace=True)

#renaming the new value column as Location Description
crimes_cleaned.rename(columns={'New Value':'Location Description'}, inplace=True)


# Pulling in Community Area Names and Regions

#reading in the mapping of the Community Area ID to the Name and Region
#values from Wikipedia
community_areas = pd.read_csv('Data/Community_Areas.csv')

#merging the community area df with the reduced crimes df
crimes_cleaned = crimes_cleaned.merge(community_areas, how='left',
                                      left_on='Community Area',
                                      right_on='ID')

#dropping the ID columns
crimes_cleaned.drop(labels=['Community Area','ID'],axis=1,inplace=True)

#renaming the Name column as Community Area
crimes_cleaned.rename(columns={'Name':'Community Area'}, inplace=True)


# Creating New Datetime Columns based on the Date of the Crime

#adding a column for the month of the crime
crimes_cleaned['Month'] = crimes_cleaned.Date.dt.month

#adding a column for the day of week of the crime
crimes_cleaned['Day of Week'] = crimes_cleaned.Date.dt.day_name()

#creating index vars for time of day (morning, afternoon, evening, and night)
morning_idx   = (crimes_cleaned.Date.dt.time >= dt.time( 5)) & (crimes_cleaned.Date.dt.time < dt.time(12)) # 5am to 12pm
afternoon_idx = (crimes_cleaned.Date.dt.time >= dt.time(10)) & (crimes_cleaned.Date.dt.time < dt.time(17)) #12pm to  5pm
evening_idx   = (crimes_cleaned.Date.dt.time >= dt.time(17)) & (crimes_cleaned.Date.dt.time < dt.time(20)) # 5pm to  8pm
night_idx     = (crimes_cleaned.Date.dt.time >= dt.time(20)) | (crimes_cleaned.Date.dt.time < dt.time( 5)) # 8pm to  5am

#adding a column for the time of day of the crime
crimes_cleaned['Time of Day'] = ""
crimes_cleaned.loc[morning_idx,   'Time of Day'] = "Morning"
crimes_cleaned.loc[afternoon_idx, 'Time of Day'] = "Afternoon"
crimes_cleaned.loc[evening_idx,   'Time of Day'] = "Evening"
crimes_cleaned.loc[night_idx,     'Time of Day'] = "Night"

#creating index vars for season of year (spring, summer, fall, winter)
spring_idx = (crimes_cleaned.Month >=  3) & (crimes_cleaned.Month <  6)
summer_idx = (crimes_cleaned.Month >=  6) & (crimes_cleaned.Month <  9)
fall_idx   = (crimes_cleaned.Month >=  9) & (crimes_cleaned.Month < 12)
winter_idx = (crimes_cleaned.Month >= 12) | (crimes_cleaned.Month <  3)

#adding a column for the season the crime occurred in
crimes_cleaned['Season'] = ""
crimes_cleaned.loc[spring_idx, 'Season'] = "Spring"
crimes_cleaned.loc[summer_idx, 'Season'] = "Summer"
crimes_cleaned.loc[fall_idx,   'Season'] = "Fall"
crimes_cleaned.loc[winter_idx, 'Season'] = "Winter"


# Dropping Nulls from the Dataset

crimes_cleaned.dropna(inplace=True,axis=0)


# Saving the Cleaned Dataset

crimes_cleaned.to_csv("Data/crimes_cleaned.csv", index=False)
