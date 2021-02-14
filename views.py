import configparser
import psycopg2
from sql_queries import views_creation


def views_deploy(cur, conn):
    for query in views_creation:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    views_deploy(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
