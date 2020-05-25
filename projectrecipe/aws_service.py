import boto3 as boto 
import read_config
import setup_logging
import datetime
import socket

config = read_config.getconfig()
log = setup_logging.getLogger() # 192.168.0.17

def getAWSSession(profile='Default'):
    log.info("Setting up AWS Session for profile: {}".format(profile))
    if profile == 'AWS': 
        session = boto.Session()
    else: 
        session = boto.Session(profile_name=profile)
    return session

def getResource(resourcename): 
    host_name, host_ip = getIPAddress()

    if 'ec2' in host_name:
        session = getAWSSession(profile='AWS')
    else:
        session = getAWSSession(profile=config['PRCONFIG']['AWS']['PROFILE'])
    
    if resourcename.upper() == 'S3': 
        try: 
            awsclient = session.client(resourcename)
        except Exception: 
            log.error("Error in getting client resource for AWS resource : {}".format(resourcename))
    else: 
        log.info("Incorrect resource name passed. Please pass in the right resource name. Acceptable: s3")

    return awsclient

def createawsbucket(bucketname): 
    awsclient = getResource('s3')
    
    try: 
        result = awsclient.create_bucket(Bucket=bucketname)
        
        log.info("AWS Log: [ {} ]".format(result))
        log.info("AWS bucket created. Bucket Name: {}".format(bucketname))
        
    except Exception:
        log.error("Error creating AWS bucket: {}".format(bucketname))


def putdataintobucket(bucketname, filename): 
    awsclient = getResource('s3')
    try: 
        out = awsclient.upload_file(Filename=filename,Bucket=bucketname,Key=filename)
        log.info("File uploaded in the AWS. Log: [ {} ]".format(out))
    except Exception: 
        log.error("Unable to upload file: {} to AWS S3 bucket : {}".format(filename,bucketname))


def getIPAddress():
    '''
        Get the IP address of the machine
    '''
    try: 
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
    except: 
        print("Unable to get Hostname and IP") 
    
    return (host_name,host_ip)



