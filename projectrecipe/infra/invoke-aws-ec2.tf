variable "region" {
    type = "string"
    default = "us-east-1"
}

variable "aws_credentials" {
    default = "/Users/rishushrivastava/.aws/credentials"
}

provider "aws" {
    profile    = "default"
    region     = var.region
}

resource "aws_s3_bucket" "projectrecipe_s3_bkt_rks_2020" {
    bucket = "projectrecipe_s3_bkt_rks_2020"
    acl="public"
}

resource "aws_instance" "projectrecipe_ec2" {
    ami="ami-0323c3dd2da7fb37d"  # generic ami for free tier
    instance_type = "t2.micro"
    key_name = "MyVMInstanceKeyPair"

    tags = {
        Name = "RSPy-ProjectRecipe"
    }
}

