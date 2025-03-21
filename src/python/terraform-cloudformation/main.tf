terraform {
  backend "s3" {
    bucket = "kkrull-at-8thlight-python-sandbox"
    key    = "terraform-cloudformation/main.tfstate"
    region = "us-east-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "aws_cloudformation_stack" "unsupported_resources" {
  name          = "cloudformation"
  template_body = file("${path.module}/sns-template.json")
}
