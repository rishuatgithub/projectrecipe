####################################################################
## General Configurations
####################################################################

profile = "default"                            
region = "us-east-1"
aws_credentials = "/Users/rishushrivastava/.aws/credentials" 

####################################################################
## AWS EC2 Instance Specific Configuration
####################################################################

aws_instance_count = 1                         
aws_ami_instance = "ami-0323c3dd2da7fb37d"
aws_instance_type = "t2.micro"                 
aws_iam_instance_profile = "projectrecipe_iam_ec2_s3_codedeploy_role" 
aws_ec2_keyname= "MyVMInstanceKeyPair"       
aws_ec2_sgrp= ["ProjectRecipeEC2-SG-01"]
aws_ec2_tag_name = "RSPy-ProjectRecipe" 
aws_ec2_userdata_file_location = "/Users/rishushrivastava/Documents/GitHub/projectrecipe/install_scripts/aws_install_codedeploy_pyenv.sh"