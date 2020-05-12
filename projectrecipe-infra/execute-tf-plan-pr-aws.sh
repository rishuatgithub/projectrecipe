#!/bin/bash

######################################################################
## This script plans and apply terraform for aws - project recipe
######################################################################

LOAD_PLAN=$1
PLAN_OUT_FILENAME="projectrecipe-aws-tf-plan.out"
VAR_FILENAME="invoke-aws-ec2.tfvars"

if [ $1 == "START" ]; then
    echo "Planning Terraform"
    terraform plan -var-file=$VAR_FILENAME --out $PLAN_OUT_FILENAME

    echo "Applying Terraform Plan"
    terraform apply -var-file=$VAR_FILENAME --auto-approve

fi 

if [ $1 == "STOP" ]; then 
    echo "Destroying Terraform Plan"
    terraform destroy -var-file=$VAR_FILENAME --auto-approve
fi

exit 0