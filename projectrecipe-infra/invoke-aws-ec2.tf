variable "profile" {}                
variable "region" {}
variable "aws_credentials" {}
variable "aws_instance_count" {}
variable "aws_ami_instance" {}
variable "aws_instance_type" {}
variable "aws_iam_instance_profile" {}
variable "aws_ec2_keyname" {}
variable "aws_ec2_sgrp" {}
variable "aws_ec2_tag_name" {}
variable "aws_ec2_userdata_file_location" {}

variable "aws_s3_bucketname" {}
variable "aws_s3_acl" {}


provider "aws" {
    profile    = var.profile
    region     = var.region
}

resource "aws_s3_bucket" "projectrecipe_s3" {
    bucket = var.aws_s3_bucketname
    acl = var.aws_s3_acl
}

resource "aws_instance" "projectrecipe_ec2" {
    count=var.aws_instance_count
    ami=var.aws_ami_instance
    instance_type = var.aws_instance_type
    key_name = var.aws_ec2_keyname
    security_groups = var.aws_ec2_sgrp
    iam_instance_profile = var.aws_iam_instance_profile

    tags = {
        Name = var.aws_ec2_tag_name
    }

    user_data = file(var.aws_ec2_userdata_file_location)
}

