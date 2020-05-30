import read_config
import logging

def getLogger(): 

    config = read_config.getconfig()

    LOGFILENAME = config['PRCONFIG']['GENERAL']['LOG_DIR'] + config['PRCONFIG']['GENERAL']['LOG_FILENAME']
    
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',filename=LOGFILENAME,filemode='w',level=logging.DEBUG, datefmt='%m/%d/%Y %H:%M:%S')

    return logging 


def getDatabaseLogger(): 

    config = read_config.getconfig()

    LOGFILENAME = config['PRCONFIG']['GENERAL']['LOG_DIR'] + config['PRCONFIG']['GENERAL']['DB_LOG_FILENAME']
    
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',filename=LOGFILENAME,filemode='w',level=logging.DEBUG, datefmt='%m/%d/%Y %H:%M:%S')

    return logging 