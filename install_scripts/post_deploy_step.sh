#!/bin/bash

################################################################
# This step prepares the project-recipe deployment
################################################################

source /home/ec2-user/projectrecipe/install_scripts/install_config.sh

echo "Project Install Dir : $EC2_HOME_DIR/$PROJECT_DIR_NAME"
echo "Project Environment Name: $ENV_NAME"

#unzip projectrecipe.zip
echo "Activating Environment"
source $EC2_HOME_DIR/$ENV_NAME/env/bin/activate

echo "Upgrade pip"
pip install --upgrade pip

echo "Installing Requirement and seting up enviornment"
pip3 install -r $EC2_HOME_DIR/$PROJECT_DIR_NAME/requirements.txt

