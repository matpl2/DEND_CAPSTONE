import configparser
import psycopg2
from sql_queries import quality_check_steps


def quality_process(cur, conn):
    for query in quality_check_steps:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    quality_process(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
