#!/usr/bin/env python
# coding: utf-8
import pymongo
import read_config
import setup_logging
import json
import sys

class MongoDBConnection:
    def __init__(self):
        self.username = config['PRCONFIG']['MONGODB']['USERNAME']
        self.password = config['PRCONFIG']['MONGODB']['PASSWORD']
        self.cluster  = config['PRCONFIG']['MONGODB']['CLUSTER']

    def get_connection(self,dbname): 
        conn_string = "mongodb+srv://"+self.username+":"+self.password+"@"+self.cluster+"?retryWrites=true&w=majority"
        #log.info(conn_string)
        try:
            client = pymongo.MongoClient(conn_string)

        except Exception as e: 
            log.error(f"Connection Failed to Database :{dbname}")
            log.error(e)
            sys.exit(1)
        
        return client[dbname]


def getMongoClientDB():
    dbname = config['PRCONFIG']['MONGODB']['DATABASE']
    return MongoDBConnection().get_connection(dbname)
    

def getAllCollections():
    list_collections = getMongoClientDB().list_collection_names()
    log.info(f"The List of Collections: {list_collections}")
    return list_collections


def insert_record_todb(collection_name, data):
    db = getMongoClientDB()
    try:
        insertdata = db[collection_name].insert_one(data)
        log.info(f"Inserted Record : {insertdata.inserted_id}")
    except Exception as e: 
        log.error(f"Error while importing data to database. {e}")
        sys.exit(1)


def insert_bulk_record_todb(collection_name, data): 
    db = getMongoClientDB()
    try:
        result = db[collection_name].insert_many(data)
        log.info(f"Total Inserted Records : {len(result.inserted_ids)}")
        log.info(f"Total Inserted IDs : {result.inserted_ids}")
    except Exception as e: 
        log.error(f"Error while importing data to database. {e}")
        sys.exit(1)


def drop_collection(col_name): 
    '''
        Dropping an existing collection for truncate load
    '''
    log.warning(f"Dropping collection : {col_name}")
    db = getMongoClientDB()
    try: 
        db[col_name].drop()
    except Exception as e: 
        log.error(f"Error while dropping collection {col_name}")
        log.error(e)


def divide_rows_into_chunks(data_list, chunk_size): 
    '''
        Divide a list into chunks for bulk insert in batches.
    '''
    for i in range(0, len(data_list), chunk_size): 
        yield data_list[i:i + chunk_size]


def parse_jo_json(filename):
    '''
        Parse indivisual file from projects
    '''

    with open(filename) as f:
        data = json.load(f)

    if 'l0' in filename:
        log.info(f"Loading Data for file: {filename}")
        insert_record_todb('jamieoliverdata_l0',data)
    
    if 'l1' in filename:
        log.info(f"Loading Data for file: {filename}")
        for d in data['data']['levels']['level1']:
            insert_record_todb('jamieoliverdata_l1',d)

    if 'l2' in filename:
        log.info(f"Loading Data for file: {filename}")
        for d in data['data']['levels']['level2']:
            insert_record_todb('jamieoliverdata_l2',d)

    if 'l3' in filename:
        log.info(f"Loading Data for file: {filename}")
        bulk_arr = []
        bulk_cntr = 0
        for d in data['data']['levels']['level3']:
            new_dict = {}
            new_dict = {'item_id':bulk_cntr,'data':d}
            bulk_arr.append(new_dict)
            bulk_cntr += 1
        
        chunked_dataset = list(divide_rows_into_chunks(bulk_arr, 500))

        for i in range(len(chunked_dataset)):
            insert_bulk_record_todb('jamieoliverdata_l3',chunked_dataset[i])
        


def databasemainjob():
    '''
        This is the main job
    '''

    for cols in getAllCollections(): 
        if 'jamieoliver' in cols: 
            drop_collection(cols)
    
    log.info("Starting Record Insertion Job to Database")
    parse_jo_json('projectrecipe/data/jamieoliverdata_l0.json')
    parse_jo_json('projectrecipe/data/jamieoliverdata_l1.json')
    parse_jo_json('projectrecipe/data/jamieoliverdata_l2.json')
    parse_jo_json('projectrecipe/data/jamieoliverdata_l3.json')

    log.info("The Job Execution for Loading raw data into DB is now complete. Check logs for more.")


if __name__ == '__main__':
    config = read_config.getconfig()
    log = setup_logging.getDatabaseLogger()
    databasemainjob()
    
    