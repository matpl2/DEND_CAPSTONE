# DEND_CAPSTONE - Serverless ETL pipeline
Capstone project for the Data Engineer NanoDegree program

Purpose of this project is to build an ETL pipeline for a data that is regulary dispatched to the S3 bucket. 


## Files
This project includes following files:
- Data floder with datasets described below
- Pictures folder with pictures respository
- License; licence used for this project
- Readme; this readme doc
- dwh.cfg; configuration file for Redshift and S3
- queries.py; SQL queries used for this project
- create_schemas.py; file that can create schema
- tables_create_copy.py; file that can create tables and load data via COPY command
- views.py; file that can create views
- file that can execute queries to check if load process delivered data to tables
- my_function.yaml; lambda function that loads flights table in the yaml format
- my_function-37febacc-743b-42ff-9d81-65d9cb6c7c42.zip; lambda function that loads flights table in the zip format


views.py

## Datasets
Dataset used in this project is stored in data/set1 folder. This dataset includes 3 files:

- airlines.txt
- airports.csv
- flights example.csv

The orginal datasets comes from: https://www.kaggle.com/usdot/flight-delays
For the purpose of this excercise orginal file airlines.csv was change dto txt format. Also, the respository includes only flights sample data due to the limitation of github. Orginal file should be downloaded from the link above.


airlines.txt

The first dataset is a short list that translates IATA air line code to the user friendly name.

airports.csv

The second dataset consists list of airports in the USA and allows to translate IATA airport code to the user friendly name. It also consist geolocation data of the airport such as longitude, latitude, state, and city.

flights example.csv

This dataset includes data about flights. A lot of details is provided for each domestic flight in the USA.


## Project scope
The goal of this project is to build ETL pipeline together with set of tables for the dummy scenario. Although scenario is dummy it is very likely that many companies will have very similar business case. In this scenario we have 3 files that are shared with us by external vendor. Vendor upload data to S3. Two of datasets (airlines.json, airports.csv) are static and do not really change frequently. Of of dataset (flights details) is very dynamic and can be uploaded to S3 multiple times per day. There is not fixed schedule for that, however what we know is that vendor is recreating dataset from the begining each time (insert/table logic). Our task is to set-up ETL pipeline together with Redshift  tables that would be later used by analytics team to run reports. 


## Architecture
In order to asnwer business need we are proposing following architecture that is based on AWS stack:

![alt text](https://github.com/matpl2/DEND_CAPSTONE/blob/main/pictures/pict.jpg)

Due to the fact that we do not know exactly schedule of file upload by vendor the idea is to utilize Lambda function that will be triggered by S3 upload trigger. This function will execute following steps:
1. Truncate exising flights table
2. Upload new data to the flighs table
3. Commit whole operation

This function will be triggered anytime when file is sent. Additionally, as we want to provide prepared dataset for the analytics team we will create flights_reporting view. Benefit of this solution is that view does not need to have refresh ETL pipeline as it will pull most recent data as soon as source tables are changed. This logic is presented below:

![alt text](https://github.com/matpl2/DEND_CAPSTONE/blob/main/pictures/inline.jpg)

## Redshift cluster creation
For the purpose of this project it is necessary to create Redshift database. Database creadentials, and server paths should be stored in dwh.cfg file. For my work I have created 2 nodes Redshift instance that run in defalut VPC. In such config it was necessary to configure VPC components to get access to Redshift(editing Security group for public access, attaching subnets to IGW).
Redshift instance used in this excercise:

ADD PICT


## Tables / Views
Using the song and event datasets, I have created a star schema optimized for queries on song play analysis. This includes the following tables.

Fact Table
1. songplays - records in event data associated with song plays i.e. records with page NextSong
   * songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
   
Dimension Tables
1. users - users in the app
   * user_id, first_name, last_name, gender, level
   
2. songs - songs in music database
   * song_id, title, artist_id, year, duration
   
3. artists - artists in music database
    * artist_id, name, location, lattitude, longitude
    
4. time - timestamps of records in songplays broken down into specific units
    * start_time, hour, day, week, month, year, weekday
    

This star schema would be the most optimal for the analytics team. Also, because orginal dataset is in S3 the most efficient way for ETL process was to use Spark on EMR to transofrm data.



## Process
In order to create this pipeline following steps were taken:
1. Redshift launch in AWS console
2. Creation of script that will create tables
3. Creation of script for upload of data
4. Creation of lambda function that will execure script from point 3
5. Creation of views


## Data Analysis
