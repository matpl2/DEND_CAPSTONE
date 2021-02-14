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
- quality_check.py; file that can execute queries to check if load process delivered data to tables
- my_function.yaml; lambda function that loads flights table in the yaml format
- my_function-37febacc-743b-42ff-9d81-65d9cb6c7c42.zip; lambda function that loads flights table in the zip format

Listed above files multiple purposes therefore it is needed to follow proper sequence when executing them. Following rules should be followed: 
1) dataset should be moved to S3 buckets and these buckets should be updated in the dwh.cfg files together with Redshift credentials.
2) Purpose of lambda funtion is to load flights data as airports and airlines does not need to be refreshed.
3. lambda function has it's own cfg file that needs to be updated.
3. Before runing the lambda function it is nesecarry to create schemas (create_schemas.py).
4. Proposed order of steps are: create schemas (create_schemas.py), create and load tables (tables_create_copy.py), check if data was loaded (quality_check.py), create views (views.py) and finally set-up lambda function that will be updating flights table.


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

This dataset includes data about flights. A lot of details is provided for each domestic flights in the USA.


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

![alt text](https://github.com/matpl2/DEND_CAPSTONE/blob/main/pictures/Redshift.png)


## Tables / Views
In this project we will create 3 tables (orginal source of data) and 2 views (optimized datasets) for the analytical team.

### Tables
1. airlines - orginal source of the airlines data. Primary key was used on the IATA_CODE as this code is unique to the airline. Table is small and it will participate in joins therefore distribution style ALL was used.

2. airports - orginal source of the airports data. Primary key was used on the IATA_CODE as this code is unique to the airport. Table is small and it will participate in joins therefore distribution style ALL was used.

3. fligths - orginal source of the flights data. Huge table with 5819079 rows. This table includes core information. We expect analytics team to do dashobards for each airline (heavy filtering on airline) thus sorkkey is put on airline. Distribution style is Even as other tables we will be joining with this dataset are distributed with ALL.


### Views
1. flights_details - detailed dataset that includes each flight details. Optimization was implementing by putting flight date to the date format. Airports details were brought from airports dataset. Airports and Airlines are avialable in the descriptive form (not the code only).

2. delayed_fligths_agg - aggregated dataset that includes only flights delayed at arrival. View provides aggregated measures like (delays, flights counts).


## Lambda function
Lambda function is set-up for the flights dataset. As this dataset changes often we want to ensure it is updated properly in our table. Lambda is triggered by the S3 bucket upload event any time we get new data. Set-up of lambda function should look like this:

![alt text](https://github.com/matpl2/DEND_CAPSTONE/blob/main/pictures/Lambda%20function.png)

Source bucket should not allow for upload of other files. 

Important note: As lambda does not have psycopg module I used customized for lambda version from: https://github.com/jkehler/awslambda-psycopg2. Python 3.6 version of this psycopg is includes in lambda function (both zip and yaml).


