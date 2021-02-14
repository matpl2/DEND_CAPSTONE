# DEND_CAPSTONE - Serverless ETL pipeline
Capstone project for the Data Engineer NanoDegree program

Purpose of this project is to build an ETL pipeline for data that is regularly dispatched to the S3 bucket. 

## Files
This project includes following files:
- Data folder with datasets described below
- Pictures folder with pictures repository
- License; licence used for this project
- Readme; this readme doc
- dwh.cfg; configuration file for Redshift and S3
- queries.py; SQL queries used for this project
- create_schemas.py; file that can create schema
- tables_create_copy.py; file that can create tables and load data via COPY command
- views.py; file that can create views
- quality_check.py; file that can execute queries to check if load process delivered data to tables
- my_function.yaml; lambda function that loads flights table in the yaml format
- my_function-37febacc-743b-42ff-9d81-65d9cb6c7c42.zip; lambda function that loads flights table in the zip format

Listed above files multiple purposes therefore it is needed to follow proper sequence when executing them. Following rules should be followed: 
1) The dataset should be moved to S3 buckets and these buckets should be updated in the dwh.cfg files together with Redshift credentials.
2) Purpose of the lambda function is to load flights data as airports and airlines do not need to be refreshed.
3. lambda function has its own cfg file that needs to be updated.
3. Before running the lambda function it is necessary to create schemas (create_schemas.py).
4. Proposed order of steps are: create schemas (create_schemas.py), create and load tables (tables_create_copy.py), check if data was loaded (quality_check.py), create views (views.py) and finally set-up lambda function that will be updating flights table.

## Datasets
Dataset used in this project is stored in the data/set1 folder. This dataset includes 3 files:

- airlines.txt
- airports.csv
- flights example.csv

The original datasets comes from: https://www.kaggle.com/usdot/flight-delays
For the purpose of this exercise original file airlines.csv was changed to txt format. Also, the repository includes only flights sample data due to the limitation of github. Original file should be downloaded from the link above.


airlines.txt

The first dataset is a short list that translates IATA airline code to the user friendly name.

airports.csv

The second dataset consists of a list of airports in the USA and allows to translate IATA airport code to the user friendly name. It also consists of geolocation data of the airport such as longitude, latitude, state, and city.

flights example.csv

This dataset includes data about flights. A lot of details are provided for each domestic flights in the USA.

## Project scope
The goal of this project is to build ETL pipeline together with a set of tables for the dummy scenario. Although the scenario is dummy it is very likely that many companies will have very similar business cases. In this scenario we have 3 files that are shared with us by an external vendor. Vendor upload data to S3. Two of the datasets (airlines.txt, airports.csv) are static and do not really change frequently. The flights dataset is very dynamic and can be uploaded to S3 multiple times per day. There is no fixed schedule for that, however what we know is that the vendor is recreating the dataset from the beginning each time (insert/table logic). Our task is to set-up ETL pipeline together with Redshift  tables that would be later used by the analytics team to run reports. 


## Architecture
In order to answer business need we are proposing following architecture that is based on AWS stack:

![alt text](https://github.com/matpl2/DEND_CAPSTONE/blob/main/pictures/pict.jpg)

Due to the fact that we do not know exactly the schedule of file upload by vendor the idea is to utilize Lambda function that will be triggered by S3 upload trigger. This function will execute following steps:
1. Truncate existing flights table
2. Upload new data to the flights table
3. Commit whole operation

This function will be triggered anytime when a file is sent. Additionally, as we want to provide a prepared dataset for the analytics team we will create flights_reporting view. Benefit of this solution is that view does not need to have a refresh ETL pipeline as it will pull most recent data as soon as source tables are changed. This logic is presented below:

![alt text](https://github.com/matpl2/DEND_CAPSTONE/blob/main/pictures/inline.jpg)

## Redshift cluster creation
For the purpose of this project it is necessary to create a Redshift database. Database credentials, and server paths should be stored in a dwh.cfg file. For my work I have created 2 node Redshift instance that run in the default VPC. In such a config it was necessary to configure VPC components to get access to Redshift(editing Security group for public access, attaching subnets to IGW).
Redshift instance used in this exercise:


![alt text](https://github.com/matpl2/DEND_CAPSTONE/blob/main/pictures/Redshift.png)


## Tables / Views
In this project we will create 3 tables (original source of data) and 2 views (optimized datasets) for the analytical team.

### Tables
1. airlines - original source of the airlines data. Primary key was used on the IATA_CODE as this code is unique to the airline. Table is small and it will participate in joins therefore the distribution style ALL was used.

2. airports - original source of the airports data. Primary key was used on the IATA_CODE as this code is unique to the airport. Table is small and it will participate in joins therefore the distribution style ALL was used.

3. flights - original source of the flights data. Huge table with 5819079 rows. This table includes core information. We expect analytics team to do dashboards for each airline (heavy filtering on airline) thus sorkkey is put on airline. Distribution style is Even as other tables we will be joining with this dataset are distributed with ALL.

### Views
1. flights_details - detailed dataset that includes each flight details. Optimization was implemented by putting the flight date to the date format. Airport details were brought from the airports dataset. Airports and Airlines are available in the descriptive form (not the code only).

2. delayed_fligths_agg - aggregated dataset that includes only flights delayed at arrival. View provides aggregated measures like (delays, flights counts).

## Lambda function
Lambda function is set-up for the flights dataset. As this dataset changes often we want to ensure it is updated properly in our table. Lambda is triggered by the S3 bucket upload event any time we get new data. Set-up of lambda function should look like this:

![alt text](https://github.com/matpl2/DEND_CAPSTONE/blob/main/pictures/Lambda%20function.png)

Source bucket should not allow for upload of other files. 

Important note: As lambda does not have a psycopg module I used customized for lambda version from: https://github.com/jkehler/awslambda-psycopg2. Python 3.6 version of this psycopg is included in lambda function (both zip and yaml).

## The write-up
For this project I have decided to use serverless (AWS lambda) solution for refreshing data. Serverless architecture becomes more and more popular and it can scale quite fast.  Views created in this project should deliver expected experience for the analytics team. Benefit of the solution with views is that there is not a delay between source table refresh and the view, additionally we can always reach original data source if we want to see data without any modification.

As a final step, I would like to cover future possible scenarios:

1. The data was increased by 100x.
In such a case we would need to ensure that we can scale our Redshift (increase the number of nodes or change node type), however Redshift will easily scale to such a challenge. As we run ETL pipeline on serverless architecture it will scale-up automatically. Process can take longer so we just need to remember to increase the lambda time-out threshold.

2.The pipelines would be run on a daily basis by 7 am every day.
Our lambda function can run several times per day already. 

3.The database needed to be accessed by 100+ people.
As mentioned in the point above we would need to ensure proper scaling of the redshift. With such a huge user pool we may also consider to replace views with tables (materialized datasets) so queries can run more efficiently.

