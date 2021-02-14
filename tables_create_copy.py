import configparser
import psycopg2
from sql_queries queries_flight, queries_airlines, queries_airports


def flights_table(cur, conn):
    for query in queries_flight:
        cur.execute(query)
        conn.commit()

def airlines_table(cur, conn):
    for query in queries_airlines:
        cur.execute(query)
        conn.commit()

def airports_table(cur, conn):
    for query in queries_airports:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    airlines_table(cur, conn)
    airports_table(cur, conn)
    flights_table(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
