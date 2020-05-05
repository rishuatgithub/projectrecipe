provider "aws" {
    access_key = ""
    secret_key = ""
    profile    = "default"
    region     = "us-east-1"
}

resource "aws_s3_bucket" "projectrecipe_s3_bkt_rks_2020" {
    bucket = "projectrecipe_s3_bkt_rks_2020"
    acl="public"
}

resource "aws_instance" "projectrecipe_ec2" {
    ami="ami-04944861fb0f3aac8"
    instance_type = "t2.micro"
    key_name = "MyVMInstanceKeyPair"

}

