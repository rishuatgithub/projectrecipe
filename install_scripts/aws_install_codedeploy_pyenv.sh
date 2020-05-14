#!/bin/bash

## This is passed as a userdata to AWS while setting up instance

################################################################
## This script installs code deploy agent into ec2 instance
################################################################

sudo yum update -y
sudo yum install ruby -y
sudo yum install wget -y 
cd /home/ec2-user
wget https://aws-codedeploy-us-east-1.s3.us-east-1.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto
sudo service codedeploy-agent start
sudo service codedeploy-agent status

################################################################
## This script installs Python3 and sets up the py env
################################################################

sudo yum install python3 -y
python3 -m venv projectrecipe/env
source ~/projectrecipe/env/bin/activate
pip install pip --upgrade
echo "source ${HOME}/projectrecipe/env/bin/activate" >> ${HOME}/.bashrc
source ~/.bashrc
