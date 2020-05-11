
variable "region" {
    default = "us-east-1"
}

variable "aws_credentials" {
    default = "/Users/rishushrivastava/.aws/credentials"
}

variable "aws_ec2_keyname" {
    default = "MyVMInstanceKeyPair"
}

variable "aws_ec2_sgrp" {
    default = "ProjectRecipeEC2-SG-01"
}

provider "aws" {
    profile    = "default"
    region     = var.region
}

resource "aws_instance" "projectrecipe_ec2" {
    count=1
    ami="ami-0323c3dd2da7fb37d"  # generic ami for free tier
    instance_type = "t2.micro"
    key_name = var.aws_ec2_keyname
    security_groups = [var.aws_ec2_sgrp]  # sg-0770d9d2f4e18d6bd
    iam_instance_profile = "projectrecipe_iam_ec2_s3_codedeploy_role"

    tags = {
        Name = "RSPy-ProjectRecipe"
    }

    user_data = file("install_scripts/aws_install_code_deploy_agent.sh")
}


