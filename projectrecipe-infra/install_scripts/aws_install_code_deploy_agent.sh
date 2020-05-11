#!/bin/bash

############################################################
## This installs aws code deploy agent onto the EC2 Agent
## Author: Rishu Shrivastava
############################################################

sudo yum update -y

sudo yum install ruby -y

sudo yum install wget -y 

cd /home/ec2-user

wget https://aws-codedeploy-us-east-1.s3.us-east-1.amazonaws.com/latest/install

chmod +x ./install

sudo ./install auto

sudo service codedeploy-agent start

sudo service codedeploy-agent status

