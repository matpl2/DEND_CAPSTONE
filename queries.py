import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# CREATE SCHEMAS
create_schema_data = ("""CREATE SCHEMA data;""")
create_schema_wbr = ("""CREATE SCHEMA wbr;""")  

# DROP TABLES
table_fligts_drop = "DROP TABLE IF EXISTS data.flights"
table_airports_drop = "DROP TABLE IF EXISTS data.airports"
table_airlines_drop = "DROP TABLE IF EXISTS data.airlines"


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
        IATA_CODE	VARCHAR (4)
        ,AIRLINE VARCHAR (144)
        ,primary key(IATA_CODE)
    )
    DISTSTYLE ALL;  
""")

table_airports_create = ("""
    CREATE TABLE IF NOT EXISTS data.airports
    (
        IATA_CODE VARCHAR(4)
        ,AIRLINE VARCHAR (144)
        ,primary key(IATA_CODE)
    )
    DISTSTYLE ALL;  
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

table_airlines_copy = ("""
    COPY {} FROM {}
    IAM_ROLE '{}'
    delimiter ','
    IGNOREHEADER 1
    region '{}';
""").format(
    'data.airlines',
    config['S3']['DATAAIRL'],
    config['IAM_ROLE']['ARN'],
    config['CLUSTER']['REGION']
    
table_airports_copy = ("""
    COPY {} FROM {}
    IAM_ROLE '{}'
    delimiter ','
    IGNOREHEADER 1
    region '{}';
""").format(
    'data.airports',
    config['S3']['DATAAIRLP'],
    config['IAM_ROLE']['ARN'],
    config['CLUSTER']['REGION']


# TRUNCATE TABLE
table_flights_truncate = (""
    TRUNCATE data.flights;
"")

table_airports_truncate = (""
    TRUNCATE data.airports;
"")
    
table_airports_truncate = (""
    TRUNCATE data.airplines;
"")

    
# CREATING VIEWS 

flights_details_view = ("""
    CREATE VIEW wbr.flights_details AS
    (
        SELECT
        DISTINCT TO_DATE(fl.day || '-' || fl.month || '-' || fl.year,'dd-mm-yyyy') as flight_date,
        fl.day_of_week as flight_day_of_week_num,
        CASE
            WHEN fl.day_of_week = '1' THEN 'MON'
            WHEN fl.day_of_week = '2' THEN 'TUE'
            WHEN fl.day_of_week = '3' THEN 'WED'
            WHEN fl.day_of_week = '4' THEN 'THU'
            WHEN fl.day_of_week = '5' THEN 'FRI'
            WHEN fl.day_of_week = '6' THEN 'SAT'
            WHEN fl.day_of_week = '7' THEN 'SUN'
       END as flight_day_of_week,
       fl.flight_number,
       fl.tail_number,
       fl.airline as airline_iata_code,
       al.airline as airline_name,
       fl.origin_airport as origin_airport_iata,
       ap1.airport as origin_airport,
       ap1.city as orgin_airport_city,
       ap1.state as orgin_airport_state,
       ap1.country as orgin_airport_country,
       ap1.latitude as orgin_airport_latitude,
       ap1.longitude as orgin_airport_longitude,
       fl.destination_airport as destination_airport_iata,
       ap2.airport as destination_airport,
       ap2.city as destination_airport_city,
       ap2.state as destination_airport_state,
       ap2.country as destination_airport_country,
       ap2.latitude as destination_airport_latitude,
       ap2.longitude as destination_airport_longitude,
       fl.diverted,
       fl.air_time,
       fl.distance,
       fl.cancelled,
       fl.cancellation_reason,
       fl.departure_delay,
       fl.arrival_delay,
       fl.air_system_delay,
       fl.security_delay,
       fl.airline_delay,
       fl.late_aircraft_delay,
       fl.weather_delay
       
       FROM  data.flights fl
       LEFT JOIN data.airlines al ON fl.airline = al.iata_code
       LEFT JOIN data.airports ap1 ON fl.origin_airport = ap1.iata_code
       LEFT JOIN data.airports ap2 ON fl.destination_airport = ap2.iata_code
)

flights_delayed_agg_view = ("""
    CREATE VIEW wbr.delayed_fligths_agg  AS
    (
        SELECT
        DISTINCT TO_DATE(fl.day || '-' || fl.month || '-' || fl.year,'dd-mm-yyyy') as flight_date,
        fl.day_of_week as flight_day_of_week_num,
        CASE
            WHEN fl.day_of_week = '1' THEN 'MON'
            WHEN fl.day_of_week = '2' THEN 'TUE'
            WHEN fl.day_of_week = '3' THEN 'WED'
            WHEN fl.day_of_week = '4' THEN 'THU'
            WHEN fl.day_of_week = '5' THEN 'FRI'
            WHEN fl.day_of_week = '6' THEN 'SAT'
            WHEN fl.day_of_week = '7' THEN 'SUN'
        END as flight_day_of_week,
        fl.airline as airline_iata_code,
        al.airline as airline_name,
        fl.origin_airport as origin_airport_iata,
        ap1.airport as origin_airport,
        ap1.city as orgin_airport_city,
        ap1.state as orgin_airport_state,
        ap1.country as orgin_airport_country,
        ap1.latitude as orgin_airport_latitude,
        ap1.longitude as orgin_airport_longitude,
        fl.destination_airport as destination_airport_iata,
        ap2.airport as destination_airport,
        ap2.city as destination_airport_city,
        ap2.state as destination_airport_state,
        ap2.country as destination_airport_country,
        ap2.latitude as destination_airport_latitude,
        ap2.longitude as destination_airport_longitude,
        fl.diverted,
        COUNT(fl.flight_number) as total_flights,
        SUM(fl.air_time) as total_air_time,
        AVG(fl.air_time) as avg_air_time,
        SUM(fl.distance) as total_distance,
        AVG(fl.distance) as avg_distance,
        SUM(fl.arrival_delay) as total_arriv_delay,
        AVG(fl.arrival_delay) as avg_arriv_delay,
        SUM(fl.air_system_delay) as total_air_system_delay,
        AVG(fl.air_system_delay) as avg_air_system_delay,
        SUM(fl.security_delay) as total_security_delay,
        AVG(fl.security_delay) as avg_security_delay,
        SUM(fl.airline_delay) as total_airline_delay,
        AVG(fl.airline_delay) as avg_airline_delay,
        SUM(fl.late_aircraft_delay) as total_late_aircraft_delay,
        AVG(fl.late_aircraft_delay) as avg_late_aircraft_delay,
        SUM(fl.weather_delay) as total_weather_delay,
        AVG(fl.weather_delay) as avg_weather_delay
        
        FROM data.flights fl
        
        LEFT JOIN data.airlines al ON fl.airline = al.iata_code
        LEFT JOIN data.airports ap1 ON fl.origin_airport = ap1.iata_code
        LEFT JOIN data.airports ap2 ON fl.destination_airport = ap2.iata_code
        
        WHERE 
        1=1
        AND cancelled = 0
        AND NVL(arrival_delay,0) > 0
        
        GROUP BY
        TO_DATE(fl.day || '-' || fl.month || '-' || fl.year,'dd-mm-yyyy'),fl.day_of_week,
        CASE
            WHEN fl.day_of_week = '1' THEN 'MON'
            WHEN fl.day_of_week = '2' THEN 'TUE'
            WHEN fl.day_of_week = '3' THEN 'WED'
            WHEN fl.day_of_week = '4' THEN 'THU'
            WHEN fl.day_of_week = '5' THEN 'FRI'
            WHEN fl.day_of_week = '6' THEN 'SAT'
            WHEN fl.day_of_week = '7' THEN 'SUN'
            END,
        fl.airline,
        al.airline,
        fl.origin_airport,
        ap1.airport,
        ap1.city,
        ap1.state,
        ap1.country,
        ap1.latitude,
        ap1.longitude,
  fl.destination_airport,
  ap2.airport,
  ap2.city,
  ap2.state,
  ap2.country,
  ap2.latitude,
  ap2.longitude,
  fl.diverted
 )

    
# QUERY LISTS

queries_start = [create_schema_data, create_schema_wbr]
queries_flight = [table_fligths_create, table_flights_truncate, table_flights_copy]
queries_airlines = [table_fligths_create, table_flights_truncate, table_flights_copy]
queries_airports = [table_airports_create, table_airports_truncate, table_airports_copy]
    

