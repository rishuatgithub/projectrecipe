variable "profile"{}
variable "region" {}
variable "aws_credentials" {}
variable "aws_ec2_keyname" {}
variable "aws_ec2_sgrp" {}

provider "aws" {
    profile    = var.profile
    region     = var.region
}

resource "aws_instance" "projectrecipe_ec2" {
    count=1
    ami="ami-0323c3dd2da7fb37d"  # generic ami for free tier
    instance_type = "t2.micro"
    key_name = var.aws_ec2_keyname
    security_groups = var.aws_ec2_sgrp  # sg-0770d9d2f4e18d6bd
    iam_instance_profile = "projectrecipe_iam_ec2_s3_codedeploy_role"

    tags = {
        Name = "RSPy-ProjectRecipe"
    }

    user_data = file("/Users/rishushrivastava/Documents/GitHub/projectrecipe/install_scripts/aws_install_code_deploy_agent.sh")
}


