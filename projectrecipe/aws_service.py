import boto3 as boto 
import read_config
import setup_logging
import datetime

config = read_config.getconfig()
log = setup_logging.getLogger()

def getAWSSession(profile='Default'): 
    log.info(f"Setting up AWS Session for profile: {profile}")
    return boto.Session(profile_name=profile)

def getResource(resourcename): 
    session = getAWSSession(profile=config['PRCONFIG']['AWS']['PROFILE'])
    
    if resourcename.upper() == 'S3': 
        try: 
            awsclient = session.client(resourcename)
        except Exception: 
            log.error(f"Error in getting client resource for AWS resource : {resourcename}")
    else: 
        log.info(f"Incorrect resource name passed. Please pass in the right resource name. Acceptable: s3")

    return awsclient

def createawsbucket(bucketname): 
    awsclient = getResource('s3')
    
    try: 
        result = awsclient.create_bucket(Bucket=bucketname)
        
        log.info(f"AWS Log: [ {result} ]")
        log.info(f"AWS bucket created. Bucket Name: {bucketname}")
        
    except Exception:
        log.error(f"Error creating AWS bucket: {bucketname}")


def putdataintobucket(bucketname, filename): 
    awsclient = getResource('s3')
    try: 
        out = awsclient.upload_file(Filename=filename,Bucket=bucketname,Key=filename)
        log.info(f"File uploaded in the AWS. Log: [ {out} ]")
    except Exception: 
        log.error(f"Unable to upload file: {filename} to AWS S3 bucket : {bucketname}")





