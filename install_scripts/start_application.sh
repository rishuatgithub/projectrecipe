#!/bin/bash

#############################################################
## Starting Application
############################################################

source /home/ec2-user/projectrecipe/install_scripts/install_config.sh

echo "Project Install Dir : $EC2_HOME_DIR/$PROJECT_DIR_NAME"
echo "Project Environment Name: $ENV_NAME"

#unzip projectrecipe.zip
echo "Activating Environment"
source $EC2_HOME_DIR/$ENV_NAME/env/bin/activate

echo "Starting Application"
cd $EC2_HOME_DIR/$PROJECT_DIR_NAME
python projectrecipe/reading_content_parallel.py