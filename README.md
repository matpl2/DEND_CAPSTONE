# DEND_CAPSTONE
Capstone project for the Data Engineer NanoDegree program

Purpose of this project is to build an ETL pipeline for a data that is regulary dispatched to the S3 bucket. 


## Files
This project includes following files:
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

 



## Data sets
Dataset used in this project is stored in data/set1 folder. This dataset includes 3 files:

- airlines.json
- airports.csv
- flights example.csv

The orginal datasets comes from: https://www.kaggle.com/usdot/flight-delays
For the purpose of this excercise orginal file airlines.csv was change dto json format. Also, the respository includes only flights sample data due to the limitation of github. Orginal file should be downloaded from the link above.


airlines.json

The first dataset is a short list that translates IATA air line code to the user friendly name.

airports.csv

The second dataset consists list of airports in the USA and allows to translate IATA airport code to the user friendly name. It also consist geolocation data of the airport such as longitude, latitude, state, and city.

flights example.csv

This dataset includes data about flights. A lot of details is provided for each domestic flight in the USA.


## Project scope
The goal of this project is to build ETL pipeline together with set of tables for the dummy scenario. Although scenario is dummy it is very likely that many companies will have very similar business case. In this scenario we have 3 files that are shared with us by external vendor. Vendor upload data to S3. Two of datasets (airlines.json, airports.csv) are static and do not really change frequently. Of of dataset (flights details) is very dynamic and can be uploaded to S3 multiple times per day. There is not fixed schedule for that, however what we know is that vendor is recreating dataset from the begining each time (insert/table logic). Our task is to set-up ETL pipeline together with Redshift  tables that would be later used by analytics team to run reports. 


## Architecture
In order to asnwer business need we are proposing following architecture that is based on AWS stack:



