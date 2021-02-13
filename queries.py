import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES
table_fligts_drop = "DROP TABLE IF EXISTS data.flights"
table_airports_drop = "DROP TABLE IF EXISTS data.airports"
table_airlines_drop = "DROP TABLE IF EXISTS data.airlines"


# CREATE SCHEMAS
create_schema_data = ("""CREATE SCHEMA data;""")
create_schema_wbr = ("""CREATE SCHEMA wbr;""")  

# CREATE TABLES
table_fligths_create = ("""
    CREATE TABLE IF NOT EXISTS data.flights
    (
        YEAR VARCHAR(6)
        ,MONTH VARCHAR(4)
        ,DAY VARCHAR(4)
        ,DAY_OF_WEEK VARCHAR(4)
        ,AIRLINE VARCHAR(4)
        ,FLIGHT_NUMBER VARCHAR(8)
        ,TAIL_NUMBER  VARCHAR(14)
        ,ORIGIN_AIRPORT VARCHAR(12)
        ,DESTINATION_AIRPORT VARCHAR(12)
        ,SCHEDULED_DEPARTURE VARCHAR(8)
        ,DEPARTURE_TIME VARCHAR(8)
        ,DEPARTURE_DELAY INT
        ,TAXI_OUT SMALLINT
        ,WHEELS_OFF VARCHAR(8)
        ,SCHEDULED_TIME VARCHAR(8)
        ,ELAPSED_TIME VARCHAR(8)
        ,AIR_TIME VARCHAR(8)
        ,DISTANCE INT
        ,WHEELS_ON VARCHAR(8)
        ,TAXI_IN VARCHAR(8)
        ,SCHEDULED_ARRIVAL VARCHAR(8)
        ,ARRIVAL_TIME VARCHAR(8)
        ,ARRIVAL_DELAY INT
        ,DIVERTED VARCHAR(2)
        ,CANCELLED VARCHAR(2)
        ,CANCELLATION_REASON VARCHAR(2)
        ,AIR_SYSTEM_DELAY INT
        ,SECURITY_DELAY INT
        ,AIRLINE_DELAY INT
        ,LATE_AIRCRAFT_DELAY INT
        ,WEATHER_DELAY INT
    )
    DISTSTYLE EVEN
    SORTKEY (AIRLINE);
""")

table_airlines_create = ("""
    CREATE TABLE IF NOT EXISTS data.airlines
    (
        YEAR VARCHAR(6)
        ,MONTH VARCHAR(4)
        ,DAY VARCHAR(4)
        ,DAY_OF_WEEK VARCHAR(4)
        ,AIRLINE VARCHAR(4)
        ,FLIGHT_NUMBER VARCHAR(8)
        ,TAIL_NUMBER  VARCHAR(14)
        ,ORIGIN_AIRPORT VARCHAR(12)
        ,DESTINATION_AIRPORT VARCHAR(12)
        ,SCHEDULED_DEPARTURE VARCHAR(8)
        ,DEPARTURE_TIME VARCHAR(8)
        ,DEPARTURE_DELAY INT
        ,TAXI_OUT SMALLINT
        ,WHEELS_OFF VARCHAR(8)
        ,SCHEDULED_TIME VARCHAR(8)
        ,ELAPSED_TIME VARCHAR(8)
        ,AIR_TIME VARCHAR(8)
        ,DISTANCE INT
        ,WHEELS_ON VARCHAR(8)
        ,TAXI_IN VARCHAR(8)
        ,SCHEDULED_ARRIVAL VARCHAR(8)
        ,ARRIVAL_TIME VARCHAR(8)
        ,ARRIVAL_DELAY INT
        ,DIVERTED VARCHAR(2)
        ,CANCELLED VARCHAR(2)
        ,CANCELLATION_REASON VARCHAR(2)
        ,AIR_SYSTEM_DELAY INT
        ,SECURITY_DELAY INT
        ,AIRLINE_DELAY INT
        ,LATE_AIRCRAFT_DELAY INT
        ,WEATHER_DELAY INT
    )
    DISTSTYLE EVEN
    SORTKEY (AIRLINE);
""")

# LOADING TABLE
table_flights_copy = ("""
    COPY {} FROM {}
    IAM_ROLE '{}'
    delimiter ','
    IGNOREHEADER 1
    region '{}';
""").format(
    'data.flights',
    config['S3']['DATA'],
    config['IAM_ROLE']['ARN'],
    config['CLUSTER']['REGION']
)

# TRUNCATE TABLE
table_flights_truncate = ("""
    TRUNCATE data.flights;
""")


# QUERY LISTS

queries_flight = [table_fligths_create, table_flights_truncate, table_flights_copy]

