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

