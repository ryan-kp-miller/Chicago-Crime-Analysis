import os
import findspark
findspark.init()

#Setting the required parameters to start up PySpark
driver_memory = '6g'
num_executors = 2
executor_memory = '1g'
pyspark_submit_args = ' --driver-memory ' + driver_memory + ' pyspark-shell'
os.environ["PYSPARK_SUBMIT_ARGS"] = pyspark_submit_args

import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, BooleanType, DoubleType, DateType
import pyspark.sql.functions as F

spark = SparkSession.builder.master("local[*]").getOrCreate()

# Defining the Dataset Schemas
crime_schema = StructType([
    StructField('id', IntegerType(), False),
    StructField('case_number', StringType(), True),
    StructField('date', StringType(), True),
    StructField('block', StringType(), True),
    StructField('iucr', StringType(), True),
    StructField('primary_type', StringType(), True),
    StructField('description', StringType(), True),
    StructField('location_description', StringType(), True),
    StructField('arrest', BooleanType(), True),
    StructField('domestic', BooleanType(), True),
    StructField('beat', StringType(), True),
    StructField('district', StringType(), True),
    StructField('ward', IntegerType(), True),
    StructField('community_area', StringType(), True),
    StructField('fbi_code', StringType(), True),
    StructField('x_coord', IntegerType(), True),
    StructField('y_coord', IntegerType(), True),
    StructField('year', IntegerType(), True),
    StructField('updated_on', DateType(), True),
    StructField('latitude', DoubleType(), True),
    StructField('longitude', DoubleType(), True),
    StructField('location', StringType(), True),
])

ca_schema = StructType([
    StructField('community_area', IntegerType(), False),
    StructField('name', StringType(), False),
    StructField('region', StringType(), False),
    StructField('pop_2010', IntegerType(), False),
])

loc_schema = StructType([
    StructField('location_description', StringType(), False),
    StructField('location_formatted', StringType(), False),
])

# read in the homicides and non-homicide crimes and append the datasets together
homicides_df = spark.read.csv('./Data/Homicides.csv', schema=crime_schema, header=True)
gen_crimes_df = spark.read.csv('./Data/Crimes_-_2001_to_Present.csv', schema=crime_schema, header=True)
crime_df = homicides_df.union(gen_crimes_df)
# crime_df = spark.read.csv('./Data/Homicides.csv', schema=crime_schema, header=True) # for testing purposes

# read in the formatted location descriptions and the community area attributes
location_desc_df = spark.read.csv("./Data/Location.csv", schema=loc_schema, header=True)
comm_area_df = spark.read.csv("./Data/Community_Areas.csv", schema=ca_schema, header=True)

# Converting `date` from String to Timestamp
crime_df = crime_df.withColumn("date", F.to_timestamp("date", "MM/dd/yyyy hh:mm:ss a"))
crime_df = crime_df.withColumn("week_day_num", F.dayofweek(crime_df.date))

crime_df.createOrReplaceTempView("crime")
location_desc_df.createOrReplaceTempView("location")
comm_area_df.createOrReplaceTempView("comm_area")

query = """
SELECT crime.date AS Date
    ,CASE WHEN (crime.primary_type = 'NON - CRIMINAL') OR (crime.primary_type = 'NON-CRIMINAL (SUBJECT SPECIFIED)') 
        THEN 'NON-CRIMINAL' ELSE crime.primary_type END AS `Primary Type`
    ,CAST(crime.arrest as INTEGER) AS Arrest
    ,crime.domestic AS Domestic
    ,YEAR(crime.date) AS Year
    ,crime.latitude AS Latitude
    ,crime.longitude AS Longitude
    ,location.location_formatted AS `Location Description`
    ,comm_area.name AS `Community Area`
    ,comm_area.region AS Region
    ,comm_area.pop_2010 AS `2010 Population`
    ,MONTH(crime.date) AS Month
    ,CASE WHEN HOUR(crime.date) BETWEEN  5 AND 12 THEN 'Morning'
          WHEN HOUR(crime.date) BETWEEN 12 AND 17 THEN 'Afternoon'
          WHEN HOUR(crime.date) BETWEEN 17 AND 20 THEN 'Evening'
          WHEN HOUR(crime.date) >= 20 OR HOUR(crime.date) < 5 THEN 'Night'
     END AS `Time of Day`

    ,CASE WHEN crime.week_day_num = 1 THEN 'Sunday'
          WHEN crime.week_day_num = 2 THEN 'Monday'
          WHEN crime.week_day_num = 3 THEN 'Tuesday'
          WHEN crime.week_day_num = 4 THEN 'Wednesday'
          WHEN crime.week_day_num = 5 THEN 'Thursday'
          WHEN crime.week_day_num = 6 THEN 'Friday'
          WHEN crime.week_day_num = 7 THEN 'Saturday'
     END AS `Day of Week`

    ,CASE WHEN MONTH(crime.date) IN ( 3,  4,  5) THEN 'Spring'
          WHEN MONTH(crime.date) IN ( 6,  7,  8) THEN 'Summer'
          WHEN MONTH(crime.date) IN ( 9, 10, 11) THEN 'Fall'
          WHEN MONTH(crime.date) IN (12,  1,  2) THEN 'Winter'
     END AS Season

FROM crime
    INNER JOIN location ON location.location_description = crime.location_description
    INNER JOIN comm_area ON comm_area.community_area = crime.community_area

WHERE YEAR(crime.date) BETWEEN 2010 AND 2019
    AND crime.date IS NOT NULL
    AND crime.latitude IS NOT NULL
    AND crime.arrest IS NOT NULL
"""


crime_sql_df = spark.sql(query)

# convert the crime type to title case for nicer looking values
crime_sql_df = crime_sql_df.withColumn('Primary Type', F.initcap(crime_sql_df['Primary Type']))

# using collect() and then converting to pandas df because it's faster
crime_dict = crime_sql_df.collect()
crime_pd_df = pd.DataFrame(crime_dict, columns=crime_sql_df.columns)
crime_pd_df.to_csv("./Data/crimes_cleaned.csv", index=False)


