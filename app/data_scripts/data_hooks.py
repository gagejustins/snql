import psycopg2
from datetime import datetime
import os
from configparser import ConfigParser

def readConfigs():
    config = ConfigParser()
    config.read('app/data_scripts/config.py')
    return config

def db_connect(DBURI=os.environ['DATABASE_URL']):
    if isinstance(DBURI, str):
        conn = psycopg2.connect(DBURI)
        return conn
    else:
        raise ValueError('DBURI param must be a string')
        return None

def list_available_sneakers(conn):
    sql = "SELECT sneaker_name, color FROM sneakers WHERE sold_at IS NULL"
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()

    sneakers = []
    for result in results:
        sneaker = ', '.join(result)
        sneakers.append(sneaker)

    return sneakers

def sneaker_event_insert(conn, sneaker_id, event_type, config):

    if config != None:
        #Validate against event_type configs
        event_types = config['CATEGORICAL']['event_types'].split(',')
        if event_type not in event_types:
            raise ValueError('event_type must be one of {}'.format(event_types))
            return None

    sql = "INSERT INTO sneaker_events VALUES (DEFAULT, %s, %s, %s)" 
    params = (event_type, sneaker_id, datetime.utcnow())

    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()

def sneaker_insert(conn, sneaker_name, color, purchase_price, manufacturer_id):

    sql = "INSERT INTO sneakers VALUES (DEFAULT, %s, %s, %s, %s, %s) RETURNING id"
    params = (sneaker_name, color, purchase_price, manufacturer_id, datetime.utcnow())
    
    cur = conn.cursor()
    cur.execute(sql, params)
    result_id = cur.fetchone()[0]
    conn.commit()

    return result_id 
