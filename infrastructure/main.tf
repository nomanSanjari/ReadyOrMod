# Terraform configuration
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region     = "ca-central-1"
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

# Configure the AWS RDS
# For storing the User data
resource "aws_db_instance" "my_rds_instance" {
  allocated_storage   = 20 # GB ( free tier )
  db_name             = "main"
  engine              = "mysql"
  engine_version      = "5.7"
  instance_class      = "db.t2.micro"
  username            = "modman"
  password            = var.rds_password
  skip_final_snapshot = true # No snapshots for now
}

# Configure the AWS S3 Bucket
# For storing the Mods
resource "aws_s3_bucket" "mods" {
  tags = {
    Name = "Mods"
  }
}


