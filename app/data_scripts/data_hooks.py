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
    sql = "select s.id, concat_ws(', ',concat_ws(' ', case when m.collaborator_name is not null then concat_ws(' x ', m.manufacturer_name, m.collaborator_name) else m.manufacturer_name end, s.sneaker_name), s.color) as sneaker from sneakers s join manufacturers m on s.manufacturer_id = m.id and s.sold_at is null and s.trashed_at is null and s.given_at is null"

    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()

    sneakers = [result for result in results]
    return sneakers

def list_available_manufacturers(conn):
    sql="SELECT id, CASE WHEN collaborator_name IS NOT NULL THEN CONCAT_WS(' x ', manufacturer_name, collaborator_name) ELSE manufacturer_name END from manufacturers ORDER BY 2"
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
 
    manufacturers = [result for result in results]
    return manufacturers

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

def manufacturer_insert(conn, manufacturer_name, collaborator_name):

    #If collaborator_name is empty, set it to NULL
    if collaborator_name == '':
        collaborator_name = None
    
    sql = "INSERT INTO manufacturers VALUES (DEFAULT, %s, %s, %s) RETURNING id"
    params = (manufacturer_name, collaborator_name, datetime.utcnow())

    cur = conn.cursor()
    cur.execute(sql, params)
    result_id = cur.fetchone()[0]
    conn.commit()

    return result_id

def sneaker_remove(conn, sneaker_id, remove_type):
    
    remove_col_mappings = {'sell': "sold_at", 'trash': "trashed_at", 'give': "given_at"}
    remove_col = remove_col_mappings[remove_type]
    
    if remove_col == "sold_at":
        sql = "UPDATE sneakers SET sold_at = %s WHERE id = %s"
    elif remove_col == "trashed_at":
        sql = "UPDATE sneakers SET trashed_at = %s WHERE id = %s"
    else:
        sql = "UPDATE sneakers SET given_at = %s WHERE id = %s"

    params = (datetime.utcnow(), sneaker_id)

    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()

    return "Executed " + sql 

