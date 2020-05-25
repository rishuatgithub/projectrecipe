#!/bin/bash

#############################################################
## Starting Application
############################################################

source ./install_config.sh

echo "Project Install Dir : $EC2_HOME_DIR/$PROJECT_DIR_NAME"
echo "Project Environment Name: $ENV_NAME"

#unzip projectrecipe.zip
echo "Activating Environment"
source $EC2_HOME_DIR/$ENV_NAME/env/bin/activate

echo "Starting Application"
python $EC2_HOME_DIR/$PROJECT_DIR_NAME/projectrecipe/reading_content_parallel.py