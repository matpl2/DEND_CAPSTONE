import configparser
import psycopg2
from queries import schemas_creation


def create_sch(cur, conn):
    for query in schemas_creation:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    create_sch(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
